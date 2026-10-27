from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine
from app.models import models  # noqa
from app.api import auth, devices, events, alerts, dashboard
from app.api.settings import router as settings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Personal Safety Monitoring System", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(devices.router)
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)
app.include_router(settings_router)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}
