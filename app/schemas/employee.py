from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str
    position: Optional[str] = None

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Employee ID cannot be empty")
        if not re.match(r"^[A-Za-z0-9_-]+$", v):
            raise ValueError("Employee ID must be alphanumeric (dashes/underscores allowed)")
        return v.upper()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Department cannot be empty")
        return v


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    position: Optional[str] = None


class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    name: str
    email: str
    department: str
    position: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EmployeeSummary(BaseModel):
    employee: EmployeeResponse
    total_days: int
    present: int
    absent: int
    late: int
    half_day: int
    attendance_rate: float
