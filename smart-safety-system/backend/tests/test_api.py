import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET"] = "test-secret"
# reset db file
dbpath = os.path.join(os.path.dirname(__file__), "..", "test.db")
if os.path.exists(dbpath):
    os.remove(dbpath)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_flow():
    # register + login
    r = client.post("/api/auth/register", json={"email": "a@b.com", "full_name": "A", "password": "secret123"})
    assert r.status_code == 200
    r = client.post("/api/auth/login", json={"email": "a@b.com", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    H = {"Authorization": f"Bearer {token}"}

    # register device
    r = client.post("/api/devices/register", json={"device_uid": "dev1", "name": "Phone"}, headers=H)
    assert r.status_code == 200
    dev_id = r.json()["id"]

    # heartbeat
    r = client.post(f"/api/devices/{dev_id}/heartbeat", json={"network_state": "wifi", "latitude": 12.9, "longitude": 77.6}, headers=H)
    assert r.status_code == 200

    # send suspicious events
    events = []
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).isoformat()
    for i in range(5):
        events.append({"event_uid": f"e{i}", "device_uid": "dev1", "event_type": "APP_LOGIN_FAILED",
                       "timestamp": ts, "severity": "MEDIUM"})
    r = client.post("/api/events/batch", json={"events": events}, headers=H)
    assert r.status_code == 200

    # alerts should exist
    r = client.get("/api/alerts", headers=H)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # dashboard summary
    r = client.get("/api/dashboard/summary", headers=H)
    assert r.status_code == 200
    assert r.json()["total_devices"] == 1

    # unauthorized
    r = client.get("/api/dashboard/summary")
    assert r.status_code == 401

    # DSA demo
    r = client.get(f"/api/dashboard/dsa?device_id={dev_id}", headers=H)
    assert r.status_code == 200
    assert "circular_queue" in r.json()

def test_unauthorized_device_access():
    # different user
    client.post("/api/auth/register", json={"email": "b@b.com", "full_name": "B", "password": "secret123"})
    r = client.post("/api/auth/login", json={"email": "b@b.com", "password": "secret123"})
    token2 = r.json()["access_token"]
    H2 = {"Authorization": f"Bearer {token2}"}
    r = client.get("/api/devices/1", headers=H2)
    assert r.status_code == 404


def test_dsa_demo():
    # register + login as a throwaway user
    client.post("/api/auth/register", json={"email": "dsa@b.com", "full_name": "DSA", "password": "secret123"})
    r = client.post("/api/auth/login", json={"email": "dsa@b.com", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    H = {"Authorization": f"Bearer {token}"}

    # unknown device id -> 404 (not a silent failure)
    r = client.get("/api/dashboard/dsa?device_id=999999", headers=H)
    assert r.status_code == 404

    # register a device and verify the demo returns the implemented structures
    r = client.post("/api/devices/register", json={"device_uid": "dsa-dev", "name": "DSA phone"}, headers=H)
    assert r.status_code == 200
    dev_id = r.json()["id"]
    r = client.get(f"/api/dashboard/dsa?device_id={dev_id}", headers=H)
    assert r.status_code == 200
    body = r.json()
    for key in ("fifo_queue", "circular_queue", "type_counts", "priority_queue"):
        assert key in body

    # unauthorized (no token) -> 401
    r = client.get(f"/api/dashboard/dsa?device_id={dev_id}")
    assert r.status_code == 401

    # another user cannot access this device's DSA state -> 404
    client.post("/api/auth/register", json={"email": "dsa2@b.com", "full_name": "DSA2", "password": "secret123"})
    r = client.post("/api/auth/login", json={"email": "dsa2@b.com", "password": "secret123"})
    token2 = r.json()["access_token"]
    r = client.get(f"/api/dashboard/dsa?device_id={dev_id}", headers={"Authorization": f"Bearer {token2}"})
    assert r.status_code == 404
