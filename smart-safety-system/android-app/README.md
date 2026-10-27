# Android App (requires Android Studio + JDK + Android SDK)

No Android SDK was available in this environment, so the mobile client is provided as a documented module rather than a compiled binary.

Recommended implementation:
- Kotlin, Room (offline event storage), WorkManager (connectivity-aware sync)
- Screens: login, status, events, settings
- Networking: Retrofit to this backend's REST API
- Location via FusedLocationProvider with runtime permissions
- Heartbeat via WorkManager periodic task POST /api/devices/{id}/heartbeat
- Offline: store events in Room with sync_status=pending; unique event_uid; call POST /api/events/batch on connectivity restore.

Endpoints used:
- POST /api/auth/login
- POST /api/devices/register
- POST /api/devices/{id}/heartbeat
- POST /api/events
- POST /api/events/batch
