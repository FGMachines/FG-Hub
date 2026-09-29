from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    device_binding: Mapped["DeviceBinding | None"] = relationship(
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan",
    )
    api_credentials: Mapped[list["ApiCredential"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
    )
    strips: Mapped[list["StripRecord"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
    )
    commands: Mapped[list["ControlCommand"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
    )


class DeviceBinding(Base):
    __tablename__ = "device_bindings"
    __table_args__ = (
        UniqueConstraint("device_fingerprint_hash", name="uq_device_binding_fingerprint"),
        UniqueConstraint("account_id", name="uq_device_binding_account"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    device_fingerprint_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    bound_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    account: Mapped[Account] = relationship(back_populates="device_binding")


class ApiCredential(Base):
    __tablename__ = "api_credentials"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    token_hint: Mapped[str] = mapped_column(String(12), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    account: Mapped[Account] = relationship(back_populates="api_credentials")


class StripRecord(Base):
    __tablename__ = "strip_records"
    __table_args__ = (
        UniqueConstraint("account_id", "client_ref_hash", name="uq_account_strip_ref"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_ref_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    online: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    account: Mapped[Account] = relationship(back_populates="strips")
    commands: Mapped[list["ControlCommand"]] = relationship(
        back_populates="strip",
        cascade="all, delete-orphan",
    )
    outlet_states: Mapped[list["StripOutletState"]] = relationship(
        back_populates="strip",
        cascade="all, delete-orphan",
    )


class StripOutletState(Base):
    __tablename__ = "strip_outlet_states"
    __table_args__ = (
        UniqueConstraint("strip_id", "outlet", name="uq_strip_outlet_state"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    strip_id: Mapped[str] = mapped_column(
        ForeignKey("strip_records.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outlet: Mapped[int] = mapped_column(Integer, nullable=False)
    known: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    on: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    strip: Mapped[StripRecord] = relationship(back_populates="outlet_states")


class ControlCommand(Base):
    __tablename__ = "control_commands"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    strip_id: Mapped[str] = mapped_column(
        ForeignKey("strip_records.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outlet: Mapped[int] = mapped_column(Integer, nullable=False)
    desired_on: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued", index=True)
    detail: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    account: Mapped[Account] = relationship(back_populates="commands")
    strip: Mapped[StripRecord] = relationship(back_populates="commands")


class ActivityLog(Base):
    __tablename__ = "activity_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[str | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    detail_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
