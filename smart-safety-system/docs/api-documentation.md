# API Documentation

See FastAPI auto-generated docs at /docs when running. Primary endpoints:
POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
GET /api/devices, POST /api/devices/register, GET /api/devices/{id}, POST /api/devices/{id}/heartbeat
GET /api/devices/{id}/location, GET /api/devices/{id}/events
POST /api/events, POST /api/events/batch, GET /api/events, GET /api/events/{id}
GET /api/alerts, GET /api/alerts/{id}, POST /api/alerts/{id}/acknowledge
GET /api/dashboard/summary, GET /api/dashboard/dsa?device_id=
GET /api/settings, PUT /api/settings
