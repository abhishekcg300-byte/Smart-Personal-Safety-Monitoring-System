# Architecture

React dashboard -> FastAPI REST -> SQLite/PostgreSQL
Android app -> REST events/heartbeat -> FastAPI
DSA engine in backend/app/dsa drives event processing, scoring prioritization, history sorting and pattern detection.
Offline events stored locally on Android and synced via batch API with unique event IDs.
