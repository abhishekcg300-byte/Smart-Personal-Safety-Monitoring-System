import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Device, SecurityEvent, LocationRecord, User, UserSettings, Alert, TrustedContact
from app.schemas.schemas import EventIn, EventBatchIn, EventOut
from app.security.auth import get_current_user
from app.services.dsa_state import get_state
from app.dsa.event_queue import EventQueue
from app.security.risk_engine import evaluate
from app.alerts.alert_manager import create_alert, deliver_email
from datetime import datetime, timezone
import os

router = APIRouter(prefix="/api/events", tags=["events"])


def _device(db, device_uid, user):
    dev = db.query(Device).filter(Device.device_uid == device_uid).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    # authorization: owner or trusted? allow owner; trusted can view but ingestion by owner
    if dev.owner_id != user.id and user.role != "trusted":
        raise HTTPException(403, "Forbidden")
    return dev


def _store_event(db, ev: EventIn, user):
    dev = _device(db, ev.device_uid, user)
    # duplicate check
    existing = db.query(SecurityEvent).filter(SecurityEvent.event_uid == ev.event_uid).first()
    if existing:
        return existing, dev, False

    se = SecurityEvent(
        event_uid=ev.event_uid,
        device_id=dev.id,
        event_type=ev.event_type,
        timestamp=ev.timestamp.replace(tzinfo=None) if ev.timestamp.tzinfo else ev.timestamp,
        severity=ev.severity or "LOW",
        latitude=ev.latitude,
        longitude=ev.longitude,
        accuracy=ev.accuracy,
        metadata_json=json.dumps(ev.metadata) if ev.metadata else None,
        sync_status="synced",
    )
    db.add(se)
    db.commit()
    db.refresh(se)

    if ev.latitude is not None and ev.longitude is not None:
        db.add(LocationRecord(device_id=dev.id, latitude=ev.latitude, longitude=ev.longitude, accuracy=ev.accuracy))
        db.commit()

    # DSA processing
    st = get_state(dev.id)
    item = {
        "event_id": se.event_uid,
        "event_type": se.event_type,
        "timestamp": se.timestamp,
        "severity": se.severity,
    }
    st["fifo"].enqueue(item)
    st["recent"].enqueue(item)
    # hash table type counts
    prev = st["type_counts"].search(se.event_type)
    st["type_counts"].insert(se.event_type, (prev or 0) + 1)
    # sliding window for failures
    if se.event_type == "APP_LOGIN_FAILED":
        exceeded = st["sliding"].add_event(se.event_type, se.timestamp.timestamp())
        if exceeded:
            # promote
            se.event_type = "REPEATED_APP_LOGIN_FAILURE"
            db.commit()

    # risk evaluation on recent 50 events for device
    recent_events_db = (db.query(SecurityEvent)
                         .filter(SecurityEvent.device_id == dev.id)
                         .order_by(SecurityEvent.timestamp.desc())
                         .limit(50).all())
    ev_list = [{"event_id": e.event_uid, "event_type": e.event_type,
                "timestamp": e.timestamp, "severity": e.severity} for e in recent_events_db]
    # settings
    settings = db.query(UserSettings).filter(UserSettings.user_id == dev.owner_id).first()
    window = settings.event_window_seconds if settings else 300
    threshold = settings.alert_threshold_score if settings else 60
    failed_thr = settings.failed_login_threshold if settings else 5
    heartbeat_to = settings.heartbeat_timeout_seconds if settings else 300
    result = evaluate(ev_list, window_seconds=window, failed_login_threshold=failed_thr)
    se.risk_score = result["score"]
    db.commit()

    # priority queue
    st["priority"].enqueue(item, priority=result["score"])

    # alert decision
    if result["score"] >= threshold:
        # avoid duplicate alert for same event
        dup = db.query(Alert).filter(Alert.event_uid == se.event_uid).first()
        if not dup:
            alert = create_alert(db, dev, se.event_uid, se.event_type, result["level"], result["score"],
                                 "; ".join(result["factors"]))
            # deliver to trusted contacts
            contacts = db.query(TrustedContact).filter(TrustedContact.user_id == dev.owner_id).all()
            for c in contacts:
                deliver_email(db, alert, c.email)

    return se, dev, True


@router.post("", response_model=EventOut)
def create_event(ev: EventIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    se, dev, _ = _store_event(db, ev, user)
    return se


@router.post("/batch")
def create_batch(batch: EventBatchIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    out = []
    for ev in batch.events:
        se, dev, created = _store_event(db, ev, user)
        out.append({"event_uid": se.event_uid, "created": created, "risk_score": se.risk_score})
    return {"processed": len(out), "results": out}


@router.get("", response_model=list[EventOut])
def list_events(device_id: int = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(SecurityEvent)
    if device_id is not None:
        dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
        if not dev:
            raise HTTPException(404, "Device not found")
        q = q.filter(SecurityEvent.device_id == device_id)
    # only user's devices
    user_dev_ids = [d.id for d in db.query(Device).filter(Device.owner_id == user.id).all()]
    q = q.filter(SecurityEvent.device_id.in_(user_dev_ids))
    return q.order_by(SecurityEvent.timestamp.desc()).limit(200).all()


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not e:
        raise HTTPException(404, "Event not found")
    dev = db.query(Device).filter(Device.id == e.device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(403, "Forbidden")
    return e


@router.get("/device/{device_id}", response_model=list[EventOut])
def device_events(device_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    return db.query(SecurityEvent).filter(SecurityEvent.device_id == device_id).order_by(SecurityEvent.timestamp.desc()).all()
