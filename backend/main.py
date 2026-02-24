from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

app = FastAPI(title="HRMS Lite API")

# Enable CORS for all origins (for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage
employee_db = {}
attendance_db = []
next_id = 1

# ==================== MODELS ====================

class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., min_length=1, description="Company employee ID")
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str

class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

class AttendanceCreate(BaseModel):
    date: date
    status: str  # Present or Absent

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    date: date
    status: str

class DashboardStats(BaseModel):
    total_employees: int
    total_present_today: int
    total_absent_today: int
    attendance_rate: float

# ==================== EMPLOYEE ENDPOINTS ====================

@app.post("/api/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate):
    global next_id
    
    # Check for duplicate employee_id
    for emp in employee_db.values():
        if emp["employee_id"] == employee.employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee ID '{employee.employee_id}' already exists"
            )
    
    # Check for duplicate email
    for emp in employee_db.values():
        if emp["email"] == employee.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{employee.email}' already exists"
            )
    
    db_employee = {
        "id": next_id,
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "email": employee.email,
        "department": employee.department
    }
    
    employee_db[next_id] = db_employee
    next_id += 1
    
    return db_employee


@app.get("/api/employees", response_model=List[EmployeeResponse])
def get_employees():
    return list(employee_db.values())


@app.get("/api/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_db[employee_id]


@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int):
    if employee_id not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employee_db[employee_id]
    return None


# ==================== ATTENDANCE ENDPOINTS ====================

@app.post("/api/attendance")
def mark_attendance(employee_id: int, attendance: AttendanceCreate):
    # Check if employee exists
    if employee_id not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if attendance already exists for this date
    for i, att in enumerate(attendance_db):
        if att["employee_id"] == employee_id and att["date"] == attendance.date:
            # Update existing
            attendance_db[i]["status"] = attendance.status
            return attendance_db[i]
    
    # Create new attendance record
    new_attendance = {
        "id": len(attendance_db) + 1,
        "employee_id": employee_id,
        "date": attendance.date,
        "status": attendance.status
    }
    attendance_db.append(new_attendance)
    return new_attendance


@app.get("/api/attendance", response_model=List[AttendanceResponse])
def get_all_attendance():
    return attendance_db


@app.get("/api/attendance/{employee_id}")
def get_employee_attendance(employee_id: int):
    if employee_id not in employee_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return [att for att in attendance_db if att["employee_id"] == employee_id]


# ==================== DASHBOARD ENDPOINTS ====================

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    today = date.today()
    total_employees = len(employee_db)
    
    # Count today's attendance
    today_attendance = [att for att in attendance_db if att["date"] == today]
    total_present = sum(1 for att in today_attendance if att["status"] == "Present")
    total_absent = sum(1 for att in today_attendance if att["status"] == "Absent")
    
    # Calculate attendance rate
    attendance_rate = (total_present / total_employees * 100) if total_employees > 0 else 0.0
    
    return {
        "total_employees": total_employees,
        "total_present_today": total_present,
        "total_absent_today": total_absent,
        "attendance_rate": round(attendance_rate, 2)
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "HRMS Lite API is running"}


# For running locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
