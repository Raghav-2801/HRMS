from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeSummary
from app.enums import AttendanceStatus

router = APIRouter(prefix="/api/employees", tags=["Employees"])


@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    # Duplicate employee_id check
    if db.query(Employee).filter(Employee.employee_id == payload.employee_id).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee ID '{payload.employee_id}' already exists",
        )
    # Duplicate email check
    if db.query(Employee).filter(Employee.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{payload.email}' is already registered",
        )
    emp = Employee(**payload.model_dump())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    search: Optional[str] = Query(None, description="Search by name, email, or employee ID"),
    department: Optional[str] = Query(None, description="Filter by department"),
    db: Session = Depends(get_db),
):
    query = db.query(Employee)
    if search:
        like = f"%{search}%"
        query = query.filter(
            Employee.name.ilike(like)
            | Employee.email.ilike(like)
            | Employee.employee_id.ilike(like)
        )
    if department:
        query = query.filter(Employee.department.ilike(department))
    return query.order_by(Employee.created_at.desc()).all()


@router.get("/departments", response_model=List[str])
def list_departments(db: Session = Depends(get_db)):
    rows = db.query(Employee.department).distinct().order_by(Employee.department).all()
    return [r[0] for r in rows]


@router.get("/{emp_id}", response_model=EmployeeResponse)
def get_employee(emp_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return emp


@router.put("/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Email conflict check (only if changing email)
    if payload.email and payload.email != emp.email:
        if db.query(Employee).filter(Employee.email == payload.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' is already registered",
            )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(emp, field, value)

    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    db.delete(emp)
    db.commit()


@router.get("/{emp_id}/summary", response_model=EmployeeSummary)
def get_employee_summary(emp_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    records = db.query(Attendance).filter(Attendance.employee_id == emp_id).all()
    total = len(records)
    present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
    absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
    late = sum(1 for r in records if r.status == AttendanceStatus.LATE)
    half_day = sum(1 for r in records if r.status == AttendanceStatus.HALF_DAY)
    rate = round((present + late + half_day) / total * 100, 1) if total > 0 else 0.0

    return EmployeeSummary(
        employee=emp,
        total_days=total,
        present=present,
        absent=absent,
        late=late,
        half_day=half_day,
        attendance_rate=rate,
    )
