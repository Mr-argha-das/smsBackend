from fastapi import  Depends, HTTPException, APIRouter
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.holiday import Holiday
from pydantic import BaseModel
from datetime import date
from bson import ObjectId
from mongoengine.errors import NotUniqueError
from collections import defaultdict

from app.schema.auth import get_current_user
attendanceRouter = APIRouter()

class StudentIn(BaseModel):
    student_id: str
    name: str
    class_name: str

class AttendanceIn(BaseModel):
    student_id: str
    date: date
    status: str

class HolidayIn(BaseModel):
    schoolId : str
    date: date
    reason: str



@attendanceRouter.post("/mark")
def mark_attendance(att: AttendanceIn, current_user: dict = Depends(get_current_user),):
    if Holiday.objects(date=att.date).first():
        raise HTTPException(status_code=400, detail="Cannot mark attendance on holiday")

    student = Student.objects(student_id=att.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if Attendance.objects(student=student, date=att.date).first():
        raise HTTPException(status_code=400, detail="Attendance already marked")

    Attendance(student=student, date=att.date, status=att.status).save()
    return {"message": "Attendance marked"}

@attendanceRouter.get("/{student_id}")
def get_attendance(student_id: str, current_user: dict = Depends(get_current_user),):
    student = Student.objects.get(id=ObjectId(student_id)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    records = Attendance.objects(student=student)
    return {"attendance": [
        {"date": str(record.date), "status": record.status} for record in records
    ]}

@attendanceRouter.post("/holiday/add")
def add_holiday(holiday: HolidayIn, current_user: dict = Depends(get_current_user),):
    if Holiday.objects(date=holiday.date).first():
        raise HTTPException(status_code=400, detail="Holiday already exists")
    Holiday(**holiday.dict()).save()
    return {"message": "Holiday added"}

@attendanceRouter.get("/holiday/list/{school_id}")
def get_holidays(school_id: str, current_user: dict = Depends(get_current_user),):
    holidays = Holiday.objects(schoolId=school_id)
    return [{"date": str(h.date), "reason": h.reason} for h in holidays]

@attendanceRouter.get("/report/{student_id}")
def attendance_report(student_id: str, start_date: date, end_date: date, current_user: dict = Depends(get_current_user),):
    student = Student.objects(student_id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    total_days = (end_date - start_date).days + 1
    holidays = Holiday.objects(date__gte=start_date, date__lte=end_date).count()
    records = Attendance.objects(student=student, date__gte=start_date, date__lte=end_date).order_by("date")

    present_days = records.filter(status="Present").count()
    absent_days = records.filter(status="Absent").count()
    leave_days = records.filter(status="Leave").count()
    effective_days = total_days - holidays

    # Prepare daily data for graph
    daily_data = []
    month_stats = defaultdict(lambda: {"Present": 0, "Absent": 0, "Leave": 0})

    for record in records:
        daily_data.append({
            "date": record.date.strftime("%Y-%m-%d"),
            "status": record.status
        })
        month_key = record.date.strftime("%Y-%m")
        month_stats[month_key][record.status] += 1

    # Find the month with most leaves
    max_leave_month = max(month_stats.items(), key=lambda x: x[1]["Leave"], default=(None, {}))

    return {
        "student_id": student.student_id,
        "name": student.name,
        "class": student.class_name,
        "from": str(start_date),
        "to": str(end_date),
        "total_days": total_days,
        "holidays": holidays,
        "effective_days": effective_days,
        "present": present_days,
        "absent": absent_days,
        "leave": leave_days,
        "attendance_percentage": round((present_days / effective_days) * 100, 2) if effective_days else 0,
        "daily": daily_data,
        "monthly_summary": month_stats,
        "most_leave_month": {
            "month": max_leave_month[0],
            "leaves": max_leave_month[1].get("Leave", 0)
        } if max_leave_month[0] else None
    }
