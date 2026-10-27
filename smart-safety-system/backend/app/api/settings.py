from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import UserSettings, Device, LocationRecord
from app.schemas.schemas import SettingsOut, SettingsIn, LocationOut
from app.security.auth import get_current_user

router = APIRouter(tags=["settings"])


@router.get("/api/settings", response_model=SettingsOut)
def get_settings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    if not s:
        s = UserSettings(user_id=user.id)
        db.add(s)
        db.commit()
        db.refresh(s)
    return s


@router.put("/api/settings", response_model=SettingsOut)
def update_settings(data: SettingsIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    s = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    if not s:
        s = UserSettings(user_id=user.id)
        db.add(s)
        db.commit()
        db.refresh(s)
    for field in ("heartbeat_timeout_seconds", "event_window_seconds", "failed_login_threshold", "alert_threshold_score", "retention_days"):
        val = getattr(data, field)
        if val is not None:
            setattr(s, field, val)
    db.commit()
    db.refresh(s)
    return s


@router.get("/api/devices/{device_id}/location")
def device_location(device_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    loc = db.query(LocationRecord).filter(LocationRecord.device_id == device_id).order_by(LocationRecord.recorded_at.desc()).first()
    if not loc:
        raise HTTPException(404, "No location")
    return {"latitude": loc.latitude, "longitude": loc.longitude, "accuracy": loc.accuracy, "recorded_at": loc.recorded_at}


@router.get("/api/devices/{device_id}/events")
def device_events_alias(device_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from app.api.events import device_events
    return device_events(device_id, db, user)
