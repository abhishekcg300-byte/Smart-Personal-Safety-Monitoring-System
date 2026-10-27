"""Configurable risk-scoring engine.

Score range 0-100. Thresholds are illustrative starting values, not
scientifically validated safety predictions.
"""

from datetime import datetime
from typing import Any

SEVERITY_WEIGHT = {"LOW": 5, "MEDIUM": 15, "HIGH": 30, "CRITICAL": 50}

EVENT_BASE_WEIGHT = {
    "NETWORK_LOST": 10,
    "HEARTBEAT_MISSED": 25,
    "APP_LOGIN_FAILED": 8,
    "REPEATED_APP_LOGIN_FAILURE": 30,
    "SUSPICIOUS_APP_ACCESS": 35,
    "LOCATION_UPDATED": 0,
    "NETWORK_RESTORED": -5,
    "DEVICE_BACK_ONLINE": -10,
}

PATTERN_BONUS = {
    "repeated_app_login_failures": 20,
    "missing_communication": 15,
    "suspicious_app_access": 20,
    "network_loss_with_auth_failures": 10,
    "high_risk_compound": 25,
}

LEVELS = [(0, 29, "LOW"), (30, 59, "MEDIUM"), (60, 79, "HIGH"), (80, 100, "CRITICAL")]


def level_for(score: int) -> str:
    for lo, hi, name in LEVELS:
        if lo <= score <= hi:
            return name
    return "CRITICAL" if score > 100 else "LOW"


def _ts(e) -> datetime:
    t = e.get("timestamp")
    if isinstance(t, datetime):
        return t
    if isinstance(t, str):
        try:
            return datetime.fromisoformat(t.replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.utcnow()


def evaluate(events: list, window_seconds: int = 300, failed_login_threshold: int = 5) -> dict:
    """Evaluate a list of event dicts. Returns score, level, factors."""
    # dedup by event_id to prevent double-counting
    seen_ids = set()
    unique = []
    for e in events:
        eid = e.get("event_id")
        if eid is not None and eid in seen_ids:
            continue
        if eid is not None:
            seen_ids.add(eid)
        unique.append(e)

    factors = []
    score = 0

    # base weights + severity
    for e in unique:
        et = e.get("event_type", "")
        sev = e.get("severity", "LOW")
        w = EVENT_BASE_WEIGHT.get(et, 5)
        sw = SEVERITY_WEIGHT.get(sev, 5)
        contrib = w + (sw // 2)
        # bounded per-event contribution
        contrib = max(-10, min(40, contrib))
        score += contrib
        factors.append(f"{et}: base {w} + severity({sev}) {sw // 2} = {contrib}")

    # sliding window for repeated failures (time-aware)
    # inline simple repeated-failure boost
    now = max((_ts(e) for e in unique), default=None)
    failed_times = sorted(_ts(e) for e in unique if e.get("event_type") in ("APP_LOGIN_FAILED",))
    if len(failed_times) >= failed_login_threshold:
        # check if within window
        if now and failed_times and (now - failed_times[-failed_login_threshold]).total_seconds() <= window_seconds:
            bonus = 15
            score += bonus
            factors.append(f"repeated_failures: {len(failed_times)} failures in window +{bonus}")

    # pattern detection
    from ..dsa.pattern_detection import detect_patterns
    pats = detect_patterns(unique)
    for p in pats:
        b = PATTERN_BONUS.get(p, 5)
        score += b
        factors.append(f"pattern {p}: +{b}")

    score = max(0, min(100, score))
    return {"score": score, "level": level_for(score), "factors": factors, "patterns": pats}
