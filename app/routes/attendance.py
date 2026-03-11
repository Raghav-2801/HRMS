from datetime import date as date_cls
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums import AttendanceStatus
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


def _build_response(record: Attendance) -> AttendanceResponse:
    return AttendanceResponse(
        id=record.id,
        employee_id=record.employee_id,
        date=record.date,
        status=record.status,
        created_at=record.created_at,
        updated_at=record.updated_at,
        employee_name=record.employee.name if record.employee else None,
        employee_code=record.employee.employee_id if record.employee else None,
    )


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(payload: AttendanceCreate, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # One record per employee per day
    existing = (
        db.query(Attendance)
        .filter(Attendance.employee_id == payload.employee_id, Attendance.date == payload.date)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Attendance already marked for {emp.name} on {payload.date}",
        )

    record = Attendance(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return _build_response(record)


@router.get("/today", response_model=List[AttendanceResponse])
def get_today_attendance(db: Session = Depends(get_db)):
    today = date_cls.today()
    records = (
        db.query(Attendance)
        .filter(Attendance.date == today)
        .order_by(Attendance.created_at.desc())
        .all()
    )
    return [_build_response(r) for r in records]


@router.get("/", response_model=List[AttendanceResponse])
def list_attendance(
    employee_id: Optional[str] = Query(None),
    from_date: Optional[date_cls] = Query(None),
    to_date: Optional[date_cls] = Query(None),
    status_filter: Optional[AttendanceStatus] = Query(None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(Attendance)
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if from_date:
        query = query.filter(Attendance.date >= from_date)
    if to_date:
        query = query.filter(Attendance.date <= to_date)
    if status_filter:
        query = query.filter(Attendance.status == status_filter)
    records = query.order_by(Attendance.date.desc()).all()
    return [_build_response(r) for r in records]


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: str, db: Session = Depends(get_db)):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    return _build_response(record)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: str, payload: AttendanceUpdate, db: Session = Depends(get_db)):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    record.status = payload.status
    db.commit()
    db.refresh(record)
    return _build_response(record)


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: str, db: Session = Depends(get_db)):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    db.delete(record)
    db.commit()
