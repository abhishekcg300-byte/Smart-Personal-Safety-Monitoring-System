from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.db import Base


def now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="owner")  # owner | trusted
    created_at = Column(DateTime, default=now)
    devices = relationship("Device", back_populates="owner")


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    device_uid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_heartbeat = Column(DateTime, nullable=True)
    last_sync = Column(DateTime, nullable=True)
    status = Column(String, default="unknown")
    created_at = Column(DateTime, default=now)
    owner = relationship("User", back_populates="devices")
    events = relationship("SecurityEvent", back_populates="device")


class TrustedContact(Base):
    __tablename__ = "trusted_contacts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    verified = Column(Boolean, default=False)


class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True)
    event_uid = Column(String, unique=True, index=True, nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    event_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    severity = Column(String, default="LOW")
    risk_score = Column(Integer, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    metadata_json = Column(Text, nullable=True)
    sync_status = Column(String, default="synced")  # pending | synced
    processed = Column(Boolean, default=False)
    device = relationship("Device", back_populates="events")
    __table_args__ = (UniqueConstraint("event_uid", name="uq_event_uid"),)


class LocationRecord(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=True)
    recorded_at = Column(DateTime, nullable=False, default=now, index=True)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    event_uid = Column(String, nullable=True, index=True)
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending|sending|sent|failed|retry
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=now)
    deliveries = relationship("AlertDeliveryAttempt", back_populates="alert")


class AlertDeliveryAttempt(Base):
    __tablename__ = "alert_delivery_attempts"
    id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)
    channel = Column(String, nullable=False)  # email|push
    status = Column(String, nullable=False)
    error = Column(Text, nullable=True)
    attempted_at = Column(DateTime, default=now)
    alert = relationship("Alert", back_populates="deliveries")


class HeartbeatHistory(Base):
    __tablename__ = "heartbeat_history"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    received_at = Column(DateTime, default=now, index=True)
    network_state = Column(String, nullable=True)


class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    heartbeat_timeout_seconds = Column(Integer, default=300)
    event_window_seconds = Column(Integer, default=300)
    failed_login_threshold = Column(Integer, default=5)
    alert_threshold_score = Column(Integer, default=60)
    retention_days = Column(Integer, default=30)
