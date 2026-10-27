from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime


class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[str] = "owner"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    class Config:
        from_attributes = True


class DeviceRegisterIn(BaseModel):
    device_uid: str
    name: str


class DeviceOut(BaseModel):
    id: int
    device_uid: str
    name: str
    status: str
    last_heartbeat: Optional[datetime] = None
    last_sync: Optional[datetime] = None
    class Config:
        from_attributes = True


class HeartbeatIn(BaseModel):
    network_state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class EventIn(BaseModel):
    event_uid: str
    device_uid: str
    event_type: str
    timestamp: datetime
    severity: Optional[str] = "LOW"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None
    metadata: Optional[dict] = None
    client_risk_score: Optional[int] = None  # ignored; server computes


class EventBatchIn(BaseModel):
    events: List[EventIn]


class EventOut(BaseModel):
    id: int
    event_uid: str
    device_id: int
    event_type: str
    timestamp: datetime
    severity: str
    risk_score: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None
    metadata_json: Optional[str] = None
    sync_status: str
    class Config:
        from_attributes = True


class LocationOut(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    recorded_at: datetime
    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    device_id: int
    event_uid: Optional[str] = None
    alert_type: str
    severity: str
    risk_score: int
    status: str
    explanation: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True


class SettingsOut(BaseModel):
    heartbeat_timeout_seconds: int
    event_window_seconds: int
    failed_login_threshold: int
    alert_threshold_score: int
    retention_days: int
    class Config:
        from_attributes = True


class SettingsIn(BaseModel):
    heartbeat_timeout_seconds: Optional[int] = None
    event_window_seconds: Optional[int] = None
    failed_login_threshold: Optional[int] = None
    alert_threshold_score: Optional[int] = None
    retention_days: Optional[int] = None
