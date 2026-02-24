from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"

# Attendance schemas
class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatus

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True

# Employee schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=50)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    attendances: List[AttendanceResponse] = []

    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

    class Config:
        from_attributes = True

# Dashboard schema
class DashboardStats(BaseModel):
    total_employees: int
    total_present_today: int
    total_absent_today: int
    attendance_rate: float
