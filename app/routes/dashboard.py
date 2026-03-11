from datetime import date as date_cls
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.enums import AttendanceStatus

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date_cls.today()

    total_employees = db.query(func.count(Employee.id)).scalar()
    total_departments = db.query(func.count(func.distinct(Employee.department))).scalar()

    # Today's attendance counts
    today_records = db.query(Attendance).filter(Attendance.date == today).all()
    today_present = sum(1 for r in today_records if r.status == AttendanceStatus.PRESENT)
    today_absent = sum(1 for r in today_records if r.status == AttendanceStatus.ABSENT)
    today_late = sum(1 for r in today_records if r.status == AttendanceStatus.LATE)
    today_half_day = sum(1 for r in today_records if r.status == AttendanceStatus.HALF_DAY)
    today_marked = len(today_records)
    today_unmarked = max(0, total_employees - today_marked)

    # Overall attendance rate (all time)
    total_records = db.query(func.count(Attendance.id)).scalar()
    effective = db.query(func.count(Attendance.id)).filter(
        Attendance.status.in_([AttendanceStatus.PRESENT, AttendanceStatus.LATE, AttendanceStatus.HALF_DAY])
    ).scalar()
    attendance_rate = round(effective / total_records * 100, 1) if total_records > 0 else 0.0

    # Department breakdown
    dept_rows = (
        db.query(Employee.department, func.count(Employee.id))
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )
    department_breakdown = [{"department": d, "count": c} for d, c in dept_rows]

    # Recent 5 employees
    recent = db.query(Employee).order_by(Employee.created_at.desc()).limit(5).all()
    recent_employees = [
        {"id": e.id, "name": e.name, "employee_id": e.employee_id, "department": e.department}
        for e in recent
    ]

    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "attendance_rate": attendance_rate,
        "today": {
            "present": today_present,
            "absent": today_absent,
            "late": today_late,
            "half_day": today_half_day,
            "marked": today_marked,
            "unmarked": today_unmarked,
        },
        "department_breakdown": department_breakdown,
        "recent_employees": recent_employees,
    }
