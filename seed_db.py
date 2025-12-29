from app.database import SessionLocal
from app.models import Lab, Booking
from datetime import datetime, timedelta

db = SessionLocal()

# Clear existing
db.query(Booking).delete()
db.query(Lab).delete()

# Create labs
labs = [
    Lab(name="Red Lab 1", description="Offensive cyber range", zone="RED", capacity=10),
    Lab(name="Yellow Lab 1", description="Staging environment", zone="YELLOW", capacity=8),
    Lab(name="Green Lab 1", description="Safe practice lab", zone="GREEN", capacity=15),
]
db.add_all(labs)
db.commit()

# Create sample bookings
now = datetime.now()
bookings = [
    Booking(
        lab_id=1,
        user_name="Team Alpha",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=3),
        status="SCHEDULED"
    ),
    Booking(
        lab_id=2,
        user_name="Team Beta",
        start_time=now + timedelta(hours=2),
        end_time=now + timedelta(hours=4),
        status="SCHEDULED"
    ),
    Booking(
        lab_id=1,
        user_name="Team Gamma",
        start_time=now + timedelta(hours=4),
        end_time=now + timedelta(hours=6),
        status="SCHEDULED"
    ),
]
db.add_all(bookings)
db.commit()
print("✓ Database seeded with demo data")
