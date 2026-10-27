from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Device, User, TrustedContact, HeartbeatHistory, UserSettings
from app.schemas.schemas import DeviceRegisterIn, DeviceOut, HeartbeatIn
from app.security.auth import get_current_user
from datetime import datetime, timezone

router = APIRouter(prefix="/api/devices", tags=["devices"])


def _status(device: Device, timeout: int = 300) -> str:
    if device.last_heartbeat is None:
        return "unknown"
    if device.last_heartbeat is None:
        return "unknown"
    delta = (datetime.now(timezone.utc).replace(tzinfo=None) - device.last_heartbeat).total_seconds()
    return "online" if delta <= timeout else ("possibly_offline" if delta <= 2 * timeout else "offline_threshold_exceeded")


@router.post("/register", response_model=DeviceOut)
def register_device(data: DeviceRegisterIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(Device).filter(Device.device_uid == data.device_uid).first():
        raise HTTPException(400, "Device already registered")
    dev = Device(device_uid=data.device_uid, name=data.name, owner_id=user.id, status="unknown")
    db.add(dev)
    db.commit()
    db.refresh(dev)
    return dev


@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db), user=Depends(get_current_user)):
    devs = db.query(Device).filter(Device.owner_id == user.id).all()
    for d in devs:
        d.status = _status(d)
    db.commit()
    return devs


@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    dev.status = _status(dev)
    db.commit()
    return dev


@router.post("/{device_id}/heartbeat", response_model=DeviceOut)
def heartbeat(device_id: int, data: HeartbeatIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    dev.last_heartbeat = now
    dev.status = "online"
    db.add(HeartbeatHistory(device_id=dev.id, network_state=data.network_state))
    if data.latitude is not None and data.longitude is not None:
        from app.models.models import LocationRecord
        db.add(LocationRecord(device_id=dev.id, latitude=data.latitude, longitude=data.longitude))
    db.commit()
    db.refresh(dev)
    return dev
