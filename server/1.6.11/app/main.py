from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import os
import re
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .models import Account, ActivityLog, ApiCredential, ControlCommand, DeviceBinding, StripRecord

app = FastAPI(title="FG Link Server", version="0.5.0")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db = Annotated[Session, Depends(get_db)]


@app.on_event("startup")
def create_schema():
    Base.metadata.create_all(bind=engine)


def _pepper() -> bytes:
    value = os.getenv("FG_LINK_TOKEN_PEPPER", "").strip()
    if not value:
        raise RuntimeError("FG_LINK_TOKEN_PEPPER is required")
    return value.encode("utf-8")


def _digest(namespace: str, value: str) -> str:
    return hmac.new(_pepper(), f"{namespace}:{value}".encode("utf-8"), hashlib.sha256).hexdigest()


def _token_hash(token: str) -> str:
    return _digest("api-token", token)


def _device_hash(device_fingerprint: str) -> str:
    return _digest("device", device_fingerprint)


def _strip_hash(client_ref: str) -> str:
    return _digest("strip", client_ref)


def _new_api_token() -> str:
    return "fgk_" + secrets.token_urlsafe(32)


def _log(db: Session, event_type: str, *, account_id: str | None = None, detail: dict | None = None):
    db.add(
        ActivityLog(
            account_id=account_id,
            event_type=event_type,
            detail_json=json.dumps(detail or {}, ensure_ascii=False, separators=(",", ":")),
        )
    )


def _panel_guard(x_fg_panel_token: Annotated[str | None, Header()] = None):
    expected = os.getenv("FG_LINK_PANEL_TOKEN", "")
    if not expected or not x_fg_panel_token or not hmac.compare_digest(expected, x_fg_panel_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Panel access denied")


PanelGuard = Annotated[None, Depends(_panel_guard)]


def _account_from_bearer(
    db: Session,
    authorization: str | None,
) -> Account:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API token")
    raw = authorization[7:].strip()
    if not raw:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API token")

    credential = db.scalar(
        select(ApiCredential).where(
            ApiCredential.token_hash == _token_hash(raw),
            ApiCredential.revoked_at.is_(None),
        )
    )
    if credential is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token")

    account = db.get(Account, credential.account_id)
    if account is None or not account.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")

    credential.last_used_at = utcnow()
    return account


class AccountCreate(BaseModel):
    device_fingerprint: str = Field(min_length=64, max_length=64)


class AccountStateChange(BaseModel):
    active: bool


class BindRequest(BaseModel):
    device_fingerprint: str = Field(min_length=16, max_length=512)


class HeartbeatRequest(BaseModel):
    device_fingerprint: str = Field(min_length=16, max_length=512)


class StripInput(BaseModel):
    client_ref: str = Field(min_length=8, max_length=256)
    display_name: str = Field(min_length=1, max_length=120)
    online: bool = False


class StripSyncRequest(BaseModel):
    device_fingerprint: str = Field(min_length=16, max_length=512)
    strips: list[StripInput] = Field(default_factory=list, max_length=64)


class PhoneRebindRequest(BaseModel):
    device_fingerprint: str = Field(min_length=64, max_length=64)


class ControlCommandCreate(BaseModel):
    outlet: int = Field(ge=1, le=4)
    on: bool


class CommandAckRequest(BaseModel):
    device_fingerprint: str = Field(min_length=16, max_length=512)
    status: str = Field(min_length=2, max_length=20)
    detail: str = Field(default="", max_length=240)


_FINGERPRINT_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_CONTROL_REF_RE = re.compile(r"^[0-9a-fA-F]{32,64}$")


def _normalize_fingerprint(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not _FINGERPRINT_RE.fullmatch(normalized):
        raise HTTPException(status_code=422, detail="Phone fingerprint must be exactly 64 hexadecimal characters")
    return normalized


def _normalize_control_ref(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not _CONTROL_REF_RE.fullmatch(normalized):
        raise HTTPException(status_code=422, detail="Invalid strip control reference")
    return normalized


def _assert_phone_binding(account: Account, device_fingerprint: str) -> DeviceBinding:
    binding = account.device_binding
    if binding is None or not binding.active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone is not provisioned")
    fingerprint_hash = _device_hash(_normalize_fingerprint(device_fingerprint))
    if not hmac.compare_digest(binding.device_fingerprint_hash, fingerprint_hash):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone binding mismatch")
    return binding


def _new_credential(db: Session, account_id: str) -> str:
    raw_token = _new_api_token()
    db.add(ApiCredential(
        account_id=account_id,
        token_hash=_token_hash(raw_token),
        token_hint=raw_token[-6:],
    ))
    return raw_token


def _account_view(account: Account) -> dict:
    binding = account.device_binding
    now = utcnow()
    online_window = int(os.getenv("FG_LINK_CONTROLLER_ONLINE_SECONDS", "90"))
    last_seen = binding.last_seen_at if binding else None
    if last_seen is not None and last_seen.tzinfo is None:
        last_seen = last_seen.replace(tzinfo=timezone.utc)
    online = bool(last_seen and (now - last_seen).total_seconds() <= online_window)
    return {
        "id": account.id,
        "display_name": account.display_name,
        "fingerprint": account.display_name,
        "active": account.active,
        "created_at": account.created_at.isoformat(),
        "device_bound": binding is not None and binding.active,
        "device_online": online,
        "last_seen_at": last_seen.isoformat() if last_seen else None,
        "strip_count": len(account.strips),
        "online_strip_count": sum(1 for item in account.strips if item.online),
    }


@app.get("/healthz")
def healthz():
    return {
        "service": "FG Link Server",
        "status": "ok",
        "time": utcnow().isoformat(),
        "mode": "relay-ready",
    }


@app.get("/api/v1/server/status")
def server_status():
    return {
        "service": "FG Link Server",
        "cloud_enabled": True,
        "direct_mttl_access": False,
        "stores_wifi_credentials": False,
        "stores_zerotier_secrets": False,
        "panel_power_control": True,
        "fingerprint_provisioning": True,
        "device_account_policy": "fingerprint-first-one-device-one-account",
        "controller_online_window_seconds": int(os.getenv("FG_LINK_CONTROLLER_ONLINE_SECONDS", "90")),
    }


@app.post("/api/v1/client/bind")
def client_bind(
    body: BindRequest,
    db: Db,
    authorization: Annotated[str | None, Header()] = None,
):
    account = _account_from_bearer(db, authorization)
    fingerprint = _normalize_fingerprint(body.device_fingerprint)
    fingerprint_hash = _device_hash(fingerprint)

    existing_for_account = db.scalar(select(DeviceBinding).where(DeviceBinding.account_id == account.id))
    if existing_for_account:
        if not hmac.compare_digest(existing_for_account.device_fingerprint_hash, fingerprint_hash):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This account is already bound to another phone",
            )
        existing_for_account.active = True
        existing_for_account.last_seen_at = utcnow()
        _log(db, "device.rebind", account_id=account.id)
        db.commit()
        return {"status": "bound", "account": _account_view(account)}

    existing_device = db.scalar(
        select(DeviceBinding).where(DeviceBinding.device_fingerprint_hash == fingerprint_hash)
    )
    if existing_device and existing_device.account_id != account.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This phone is already bound to another account",
        )

    binding = DeviceBinding(
        account_id=account.id,
        device_fingerprint_hash=fingerprint_hash,
        active=True,
        last_seen_at=utcnow(),
    )
    db.add(binding)
    _log(db, "device.bind", account_id=account.id)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One phone can own only one FG Link account",
        )
    db.refresh(account)
    return {"status": "bound", "account": _account_view(account)}


@app.post("/api/v1/client/heartbeat")
def client_heartbeat(
    body: HeartbeatRequest,
    db: Db,
    authorization: Annotated[str | None, Header()] = None,
):
    account = _account_from_bearer(db, authorization)
    binding = _assert_phone_binding(account, body.device_fingerprint)
    binding.last_seen_at = utcnow()
    db.commit()
    return {"status": "ok", "account_id": account.id, "active": account.active}


@app.post("/api/v1/client/strips/sync")
def sync_strips(
    body: StripSyncRequest,
    db: Db,
    authorization: Annotated[str | None, Header()] = None,
):
    account = _account_from_bearer(db, authorization)
    binding = _assert_phone_binding(account, body.device_fingerprint)
    binding.last_seen_at = utcnow()
    seen_refs: set[str] = set()
    for item in body.strips:
        control_ref = _normalize_control_ref(item.client_ref)
        seen_refs.add(control_ref)
        record = db.scalar(
            select(StripRecord).where(
                StripRecord.account_id == account.id,
                StripRecord.client_ref_hash == control_ref,
            )
        )
        if record is None:
            record = StripRecord(
                account_id=account.id,
                client_ref_hash=control_ref,
                display_name=item.display_name,
            )
            db.add(record)
        record.display_name = item.display_name
        record.online = item.online
        record.last_seen_at = utcnow()

    # Remove obsolete records, including legacy rows that stored a server-side
    # digest of the local MAC. New Android builds publish only random opaque
    # control references; raw MAC addresses never reach the VPS.
    for record in list(account.strips):
        if record.client_ref_hash not in seen_refs:
            db.delete(record)

    # Deliver only tightly scoped outlet actions for this account. The phone
    # remains the local safety boundary and performs the actual MTTL operation.
    now = utcnow()
    ttl_seconds = max(30, int(os.getenv("FG_LINK_COMMAND_TTL_SECONDS", "120")))
    cutoff = now - timedelta(seconds=ttl_seconds)
    outlet_actions = []
    pending = db.scalars(
        select(ControlCommand).where(
            ControlCommand.account_id == account.id,
            ControlCommand.status.in_(("queued", "sent")),
        ).order_by(ControlCommand.created_at.asc()).limit(20)
    ).all()
    for command in pending:
        created_at = command.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if created_at < cutoff:
            command.status = "expired"
            command.completed_at = now
            command.detail = "Action TTL expired before delivery"
            continue
        if command.strip is None or not command.strip.online:
            continue
        command.status = "sent"
        if command.delivered_at is None:
            command.delivered_at = now
        outlet_actions.append({
            "id": command.id,
            "client_ref": command.strip.client_ref_hash,
            "outlet": command.outlet,
            "on": command.desired_on,
        })

    _log(db, "strips.sync", account_id=account.id, detail={"count": len(body.strips)})
    db.commit()
    return {
        "status": "ok",
        "count": len(body.strips),
        "outlet_actions": outlet_actions,
    }


@app.get("/panel", response_class=HTMLResponse, dependencies=[Depends(_panel_guard)])
def panel():
    return PANEL_HTML


@app.get("/panel/api/accounts", dependencies=[Depends(_panel_guard)])
def panel_accounts(db: Db):
    accounts = db.scalars(select(Account).order_by(Account.created_at.desc())).unique().all()
    return {"accounts": [_account_view(account) for account in accounts]}


@app.post("/panel/api/accounts", dependencies=[Depends(_panel_guard)])
def panel_create_account(body: AccountCreate, db: Db):
    fingerprint = _normalize_fingerprint(body.device_fingerprint)
    fingerprint_hash = _device_hash(fingerprint)
    existing = db.scalar(
        select(DeviceBinding).where(DeviceBinding.device_fingerprint_hash == fingerprint_hash)
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="This phone fingerprint is already provisioned")

    # The privacy-reduced 64-char app fingerprint replaces customer names.
    account = Account(display_name=fingerprint)
    db.add(account)
    db.flush()
    db.add(DeviceBinding(
        account_id=account.id,
        device_fingerprint_hash=fingerprint_hash,
        active=True,
        last_seen_at=None,
    ))
    raw_token = _new_credential(db, account.id)
    _log(db, "account.create", account_id=account.id, detail={"fingerprint_hint": fingerprint[-12:]})
    db.commit()
    db.refresh(account)
    return {"account": _account_view(account), "api_token": raw_token}


@app.post("/panel/api/accounts/{account_id}/rotate-token", dependencies=[Depends(_panel_guard)])
def panel_rotate_token(account_id: str, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    now = utcnow()
    active_credentials = db.scalars(
        select(ApiCredential).where(
            ApiCredential.account_id == account_id,
            ApiCredential.revoked_at.is_(None),
        )
    ).all()
    for credential in active_credentials:
        credential.revoked_at = now

    raw_token = _new_api_token()
    db.add(
        ApiCredential(
            account_id=account_id,
            token_hash=_token_hash(raw_token),
            token_hint=raw_token[-6:],
        )
    )
    _log(db, "api.rotate", account_id=account_id)
    db.commit()
    return {"api_token": raw_token}


@app.post("/panel/api/accounts/{account_id}/state", dependencies=[Depends(_panel_guard)])
def panel_set_account_state(account_id: str, body: AccountStateChange, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    account.active = body.active
    _log(db, "account.state", account_id=account_id, detail={"active": body.active})
    db.commit()
    return {"account": _account_view(account)}


@app.post("/panel/api/accounts/{account_id}/unbind", dependencies=[Depends(_panel_guard)])
def panel_unbind(account_id: str, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    binding = account.device_binding
    if binding is not None:
        db.delete(binding)
    now = utcnow()
    for credential in db.scalars(
        select(ApiCredential).where(
            ApiCredential.account_id == account_id,
            ApiCredential.revoked_at.is_(None),
        )
    ).all():
        credential.revoked_at = now
    _log(db, "device.unbind", account_id=account_id, detail={"tokens_revoked": True})
    db.commit()
    return {"status": "unbound", "tokens_revoked": True}


@app.post("/panel/api/accounts/{account_id}/rebind", dependencies=[Depends(_panel_guard)])
def panel_rebind_phone(account_id: str, body: PhoneRebindRequest, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    fingerprint = _normalize_fingerprint(body.device_fingerprint)
    fingerprint_hash = _device_hash(fingerprint)
    duplicate = db.scalar(
        select(DeviceBinding).where(
            DeviceBinding.device_fingerprint_hash == fingerprint_hash,
            DeviceBinding.account_id != account_id,
        )
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="This phone fingerprint is already provisioned")

    if account.device_binding is None:
        db.add(DeviceBinding(
            account_id=account.id,
            device_fingerprint_hash=fingerprint_hash,
            active=True,
            last_seen_at=None,
        ))
    else:
        account.device_binding.device_fingerprint_hash = fingerprint_hash
        account.device_binding.active = True
        account.device_binding.bound_at = utcnow()
        account.device_binding.last_seen_at = None
    account.display_name = fingerprint

    now = utcnow()
    for credential in db.scalars(
        select(ApiCredential).where(
            ApiCredential.account_id == account_id,
            ApiCredential.revoked_at.is_(None),
        )
    ).all():
        credential.revoked_at = now
    raw_token = _new_credential(db, account_id)
    _log(db, "device.rebind.admin", account_id=account_id, detail={"fingerprint_hint": fingerprint[-12:]})
    db.commit()
    return {"account": _account_view(account), "api_token": raw_token}


@app.get("/panel/api/accounts/{account_id}/strips", dependencies=[Depends(_panel_guard)])
def panel_account_strips(account_id: str, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "strips": [
            {
                "id": item.id,
                "display_name": item.display_name,
                "online": item.online,
                "last_seen_at": item.last_seen_at.isoformat() if item.last_seen_at else None,
                "last_command": (
                    {
                        "status": item.commands[-1].status,
                        "outlet": item.commands[-1].outlet,
                        "on": item.commands[-1].desired_on,
                        "completed_at": item.commands[-1].completed_at.isoformat()
                            if item.commands[-1].completed_at else None,
                    }
                    if item.commands else None
                ),
            }
            for item in account.strips
        ]
    }


@app.post("/panel/api/accounts/{account_id}/strips/{strip_id}/commands", dependencies=[Depends(_panel_guard)])
def panel_queue_command(account_id: str, strip_id: str, body: ControlCommandCreate, db: Db):
    account = db.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    if not account.active:
        raise HTTPException(status_code=409, detail="Account is disabled")
    strip = db.get(StripRecord, strip_id)
    if strip is None or strip.account_id != account_id:
        raise HTTPException(status_code=404, detail="Strip not found")
    if not strip.online:
        raise HTTPException(status_code=409, detail="Strip is offline")

    command = ControlCommand(
        account_id=account_id,
        strip_id=strip_id,
        outlet=body.outlet,
        desired_on=body.on,
        status="queued",
    )
    db.add(command)
    _log(db, "control.queued", account_id=account_id, detail={
        "strip_id": strip_id,
        "outlet": body.outlet,
        "on": body.on,
    })
    db.commit()
    db.refresh(command)
    return {"command_id": command.id, "status": command.status}


@app.post("/api/v1/client/commands/poll")
def client_poll_commands(
    body: HeartbeatRequest,
    db: Db,
    authorization: Annotated[str | None, Header()] = None,
):
    account = _account_from_bearer(db, authorization)
    binding = _assert_phone_binding(account, body.device_fingerprint)
    binding.last_seen_at = utcnow()

    now = utcnow()
    ttl_seconds = max(30, int(os.getenv("FG_LINK_COMMAND_TTL_SECONDS", "120")))
    cutoff = now - timedelta(seconds=ttl_seconds)
    pending = db.scalars(
        select(ControlCommand).where(
            ControlCommand.account_id == account.id,
            ControlCommand.status.in_(("queued", "sent")),
        ).order_by(ControlCommand.created_at.asc()).limit(20)
    ).all()

    commands = []
    for command in pending:
        created_at = command.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if created_at < cutoff:
            command.status = "expired"
            command.completed_at = now
            command.detail = "Command TTL expired before execution"
            continue
        if command.strip is None:
            command.status = "failed"
            command.completed_at = now
            command.detail = "Strip record no longer exists"
            continue
        command.status = "sent"
        if command.delivered_at is None:
            command.delivered_at = now
        commands.append({
            "id": command.id,
            "client_ref": command.strip.client_ref_hash,
            "outlet": command.outlet,
            "on": command.desired_on,
        })

    db.commit()
    return {"commands": commands}


@app.post("/api/v1/client/commands/{command_id}/ack")
def client_ack_command(
    command_id: str,
    body: CommandAckRequest,
    db: Db,
    authorization: Annotated[str | None, Header()] = None,
):
    account = _account_from_bearer(db, authorization)
    binding = _assert_phone_binding(account, body.device_fingerprint)
    binding.last_seen_at = utcnow()
    command = db.get(ControlCommand, command_id)
    if command is None or command.account_id != account.id:
        raise HTTPException(status_code=404, detail="Command not found")

    normalized_status = body.status.strip().lower()
    if normalized_status not in {"success", "failed"}:
        raise HTTPException(status_code=422, detail="Command status must be success or failed")
    command.status = "completed" if normalized_status == "success" else "failed"
    command.detail = body.detail.strip()
    command.completed_at = utcnow()
    _log(db, "control.ack", account_id=account.id, detail={
        "command_id": command.id,
        "status": command.status,
        "detail": command.detail[:120],
    })
    db.commit()
    return {"status": command.status}


@app.post("/api/v1/controllers/phone/commands/{command_id}/ack")
def phone_outlet_action_ack(
    command_id: str,
    body: dict,
    db: Db,
    x_controller_key: Annotated[str | None, Header()] = None,
):
    raw = (x_controller_key or "").strip()
    if not raw:
        raise HTTPException(status_code=401, detail="Missing phone API token")
    credential = db.scalar(
        select(ApiCredential).where(
            ApiCredential.token_hash == _token_hash(raw),
            ApiCredential.revoked_at.is_(None),
        )
    )
    if credential is None:
        raise HTTPException(status_code=401, detail="Invalid phone API token")
    account = db.get(Account, credential.account_id)
    if account is None or not account.active:
        raise HTTPException(status_code=403, detail="Account disabled")
    command = db.get(ControlCommand, command_id)
    if command is None or command.account_id != account.id:
        raise HTTPException(status_code=404, detail="Action not found")

    normalized_status = str(body.get("status", "")).strip().lower()
    if normalized_status not in {"success", "failed"}:
        raise HTTPException(status_code=422, detail="Action status must be success or failed")
    command.status = "completed" if normalized_status == "success" else "failed"
    command.detail = str(body.get("detail", ""))[:240].strip()
    command.completed_at = utcnow()
    credential.last_used_at = utcnow()
    _log(db, "control.ack", account_id=account.id, detail={
        "command_id": command.id,
        "status": command.status,
        "detail": command.detail[:120],
    })
    db.commit()
    return {"status": command.status}


@app.get("/panel/api/activity", dependencies=[Depends(_panel_guard)])
def panel_activity(db: Db, limit: int = 100):
    limit = max(1, min(limit, 300))
    rows = db.scalars(select(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(limit)).all()
    return {
        "events": [
            {
                "id": row.id,
                "account_id": row.account_id,
                "event_type": row.event_type,
                "detail": json.loads(row.detail_json or "{}"),
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    }



from pathlib import Path
PANEL_HTML = (Path(__file__).with_name("panel.html")).read_text(encoding="utf-8")
