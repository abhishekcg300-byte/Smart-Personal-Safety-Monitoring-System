import os, smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.models import Alert, AlertDeliveryAttempt, TrustedContact, Device


def _smtp_configured() -> bool:
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_FROM"))


def create_alert(db: Session, device: Device, event_uid, alert_type, severity, risk_score, explanation) -> Alert:
    alert = Alert(device_id=device.id, event_uid=event_uid, alert_type=alert_type,
                  severity=severity, risk_score=risk_score, explanation=explanation,
                  status="pending")
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def deliver_email(db: Session, alert: Alert, to_email: str) -> str:
    alert.status = "sending"
    db.commit()
    attempt = AlertDeliveryAttempt(alert_id=alert.id, channel="email", status="attempting")
    db.add(attempt)
    db.commit()
    if not _smtp_configured():
        attempt.status = "failed"
        attempt.error = "SMTP not configured"
        alert.status = "failed"
        db.commit()
        return "failed"
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Safety Alert: {alert.alert_type} (risk {alert.risk_score})"
        msg["From"] = os.getenv("SMTP_FROM")
        msg["To"] = to_email
        msg.set_content(f"Alert {alert.id}: {alert.alert_type}\nSeverity: {alert.severity}\nRisk: {alert.risk_score}\n{alert.explanation}")
        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", "587"))) as s:
            s.starttls()
            if os.getenv("SMTP_USER"):
                s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS", ""))
            s.send_message(msg)
        attempt.status = "sent"
        alert.status = "sent"
        db.commit()
        return "sent"
    except Exception as e:
        attempt.status = "failed"
        attempt.error = str(e)
        alert.status = "failed"
        db.commit()
        return "failed"
