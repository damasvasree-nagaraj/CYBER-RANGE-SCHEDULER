from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from models import LabZone, BookingStatus, UserRole


class UserCreate(BaseModel):
    name: str
    email: str
    role: UserRole = UserRole.STUDENT


class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class LabCreate(BaseModel):
    name: str
    zone: LabZone
    description: str | None = None


class LabOut(BaseModel):
    id: UUID
    name: str
    zone: LabZone
    description: str | None

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    user_id: str
    lab_id: str  
    vm_pool_id: str = "default"
    start_time: datetime
    end_time: datetime


class BookingOut(BaseModel):
    id: UUID
    user_id: UUID
    lab_id: UUID
    vm_pool_id: UUID
    start_time: datetime
    end_time: datetime
    status: BookingStatus

    class Config:
        from_attributes = True
