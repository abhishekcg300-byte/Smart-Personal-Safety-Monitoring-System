from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Device, SecurityEvent, Alert, LocationRecord
from app.security.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    devs = db.query(Device).filter(Device.owner_id == user.id).all()
    dev_ids = [d.id for d in devs]
    online = 0
    missing = 0
    for d in devs:
        if d.last_heartbeat is not None:
            from datetime import datetime
            delta = (datetime.now() - d.last_heartbeat).total_seconds() if False else (datetime.utcnow() - d.last_heartbeat).total_seconds()
            to = 300
            if delta <= to:
                online += 1
            else:
                missing += 1
        else:
            missing += 1
    pending_alerts = db.query(Alert).filter(Alert.device_id.in_(dev_ids), Alert.status.in_(["pending", "failed", "retry"])).count()
    high = db.query(SecurityEvent).filter(SecurityEvent.device_id.in_(dev_ids), SecurityEvent.risk_score >= 60).count()
    last_sync = max((d.last_sync for d in devs if d.last_sync), default=None)
    recent = db.query(SecurityEvent).filter(SecurityEvent.device_id.in_(dev_ids)).order_by(SecurityEvent.timestamp.desc()).limit(10).all()
    return {
        "total_devices": len(devs),
        "online_devices": online,
        "missing_heartbeats": missing,
        "pending_alerts": pending_alerts,
        "high_risk_events": high,
        "last_sync": last_sync,
        "recent_events": [
            {"id": e.id, "event_type": e.event_type, "timestamp": e.timestamp, "risk_score": e.risk_score,
             "severity": e.severity, "device_id": e.device_id} for e in recent
        ],
    }


@router.get("/dsa")
def dsa_demo(device_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from app.services.dsa_state import get_state
    dev = db.query(Device).filter(Device.id == device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    st = get_state(dev.id)
    fq = st["fifo"]
    cq = st["recent"]
    ht = st["type_counts"]
    pq = st["priority"]
    return {
        "fifo_queue": fq.to_list(),
        "circular_queue": cq.to_list(),
        "type_counts": ht.items(),
        "priority_queue": pq.to_list(),
    }
