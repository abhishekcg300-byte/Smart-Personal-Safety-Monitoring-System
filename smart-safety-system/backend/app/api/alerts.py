from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.models import Alert, Device
from app.schemas.schemas import AlertOut
from app.security.auth import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    dev_ids = [d.id for d in db.query(Device).filter(Device.owner_id == user.id).all()]
    return db.query(Alert).filter(Alert.device_id.in_(dev_ids)).order_by(Alert.created_at.desc()).all()


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        raise HTTPException(404, "Alert not found")
    dev = db.query(Device).filter(Device.id == a.device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(403, "Forbidden")
    return a


@router.post("/{alert_id}/acknowledge")
def ack(alert_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        raise HTTPException(404, "Alert not found")
    dev = db.query(Device).filter(Device.id == a.device_id, Device.owner_id == user.id).first()
    if not dev:
        raise HTTPException(403, "Forbidden")
    a.status = "acknowledged"
    db.commit()
    return {"ok": True}
