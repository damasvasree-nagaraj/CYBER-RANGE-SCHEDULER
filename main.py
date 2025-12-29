from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.sql import func
from fastapi.responses import HTMLResponse
from pathlib import Path

from database import Base, engine, SessionLocal
from routers.labs import router as labs_router
from routers.bookings import router as bookings_router
import models
from models import Lab, Booking, BookingStatus, AuditLog

# ---------- DB SETUP ----------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Range Scheduler API")

# ---------- CORS (FIXES "FAILED TO FETCH") ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- AUTO STATUS UPDATE LOGIC ----------
scheduler = BackgroundScheduler()

def update_booking_status():
    """Auto-update expired bookings to MAINTENANCE_WIPING and log it."""
    db = SessionLocal()
    try:
        expired = (
            db.query(models.Booking)
            .filter(
                models.Booking.end_time <= func.now(),
                models.Booking.status != models.BookingStatus.MAINTENANCE_WIPING,
            )
            .all()
        )

        for booking in expired:
            old_status = booking.status
            booking.status = models.BookingStatus.MAINTENANCE_WIPING

            log = models.AuditLog(
                booking_id=booking.id,
                action="STATUS_CHANGE",
                details=f"{old_status} -> {booking.status}",
            )
            db.add(log)

            print(
                f"[SYSTEM] Booking {booking.id} expired: "
                f"{old_status} -> {booking.status}"
            )

        db.commit()
    finally:
        db.close()

scheduler.add_job(update_booking_status, "interval", seconds=30)
scheduler.start()

# ---------- ROUTERS ----------
app.include_router(labs_router)
app.include_router(bookings_router)

# ---------- FRONTEND ----------
@app.get("/", response_class=HTMLResponse)
def frontend():
    html_path = Path(__file__).resolve().parent / "frontend.html"
    return html_path.read_text(encoding="utf-8")

# ---------- METRICS ----------
@app.get("/metrics")
def get_metrics():
    db = SessionLocal()
    try:
        return {
            "total_labs": db.query(models.Lab).count(),
            "total_bookings": db.query(models.Booking).count(),
            "active_bookings": db.query(models.Booking)
            .filter(models.Booking.status == models.BookingStatus.ACTIVE)
            .count(),
            "labs_in_maintenance": db.query(models.Booking)
            .filter(
                models.Booking.status == models.BookingStatus.MAINTENANCE_WIPING
            )
            .count(),
        }
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}
