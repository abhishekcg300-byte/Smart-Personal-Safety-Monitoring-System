# Smart Personal Safety and Security Monitoring System

A DSA-centered personal safety monitoring system: Android (documented module), FastAPI backend, React dashboard, custom DSA engine, offline sync, and trusted-contact email alerts.

## Quick Start (Backend)
```
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

## Web Dashboard
```
cd web-dashboard
npm install
npm run dev
```

## Tests
```
cd backend && pytest -q
```

## Known Limitations
- Regular Android apps cannot reliably detect every incorrect system lock-screen PIN attempt or the exact moment a phone is powered off; heartbeat-based detection is used instead.
- Camera capture is optional and not implemented in this build.
- Location is shown as last-known historical data when offline.
