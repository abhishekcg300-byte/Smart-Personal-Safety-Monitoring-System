"""Rule-based pattern detection over sequences of events.

Pattern: repeated app auth failures + heartbeat missed + suspicious app access
within a short window => elevated risk. Each rule is documented and applied only
when its conditions actually hold.
"""


def detect_patterns(events: list) -> list:
    """Return list of detected pattern names. events: list of dicts with keys
    'event_type' and 'timestamp'.
    """
    types = [e.get("event_type") for e in events]
    patterns = []
    if types.count("APP_LOGIN_FAILED") >= 3 or types.count("REPEATED_APP_LOGIN_FAILURE") >= 1:
        patterns.append("repeated_app_login_failures")
    if "HEARTBEAT_MISSED" in types:
        patterns.append("missing_communication")
    if "SUSPICIOUS_APP_ACCESS" in types:
        patterns.append("suspicious_app_access")
    if "NETWORK_LOST" in types and "APP_LOGIN_FAILED" in types:
        patterns.append("network_loss_with_auth_failures")
    # compound
    if ("repeated_app_login_failures" in patterns
            and "missing_communication" in patterns):
        patterns.append("high_risk_compound")
    return patterns
