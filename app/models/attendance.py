import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.database import Base
from app.enums import AttendanceStatus


def generate_uuid():
    return str(uuid.uuid4())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(String, primary_key=True, default=generate_uuid)
    employee_id = Column(String, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SAEnum(AttendanceStatus), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    employee = relationship("Employee", back_populates="attendances")
