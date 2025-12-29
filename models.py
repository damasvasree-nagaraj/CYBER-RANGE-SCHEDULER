from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Text,
    Enum,
    ForeignKey,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from database import Base


class LabZone(str, enum.Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


class BookingStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    MAINTENANCE_WIPING = "MAINTENANCE_WIPING"


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Lab(Base):
    __tablename__ = "labs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    zone = Column(Enum(LabZone), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class VMPool(Base):
    __tablename__ = "vm_pools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lab_id = Column(UUID(as_uuid=True), ForeignKey("labs.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    max_instances = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lab_id = Column(UUID(as_uuid=True), ForeignKey("labs.id", ondelete="CASCADE"), nullable=False)
    vm_pool_id = Column(UUID(as_uuid=True), ForeignKey("vm_pools.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id", ondelete="SET NULL"))
    action = Column(String(50), nullable=False)
    details = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
