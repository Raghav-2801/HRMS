from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from app.enums import AttendanceStatus


class AttendanceCreate(BaseModel):
    employee_id: str
    date: date
    status: AttendanceStatus

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        from datetime import date as date_cls
        if v > date_cls.today():
            raise ValueError("Cannot mark attendance for a future date")
        return v


class AttendanceUpdate(BaseModel):
    status: AttendanceStatus


class AttendanceResponse(BaseModel):
    id: str
    employee_id: str
    date: date
    status: AttendanceStatus
    created_at: datetime
    updated_at: datetime
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None

    model_config = {"from_attributes": True}
