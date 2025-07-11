from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from bson import ObjectId
from datetime import datetime, timedelta, date
from app.models.attendance import Attendance
from mongoengine.queryset.visitor import Q
import csv
from io import StringIO

attendanceAnalytcsModule = APIRouter()

# ✅ Utility: Export to CSV
def export_to_csv(data: list, columns: list):
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=attendance.csv"
    })

# ✅ 1. Daily Summary Pie Chart
@attendanceAnalytcsModule.get("/report/attendance/summary")
def attendance_summary(school_id: str, date_str: str = None):
    query_date = datetime.fromisoformat(date_str).date() if date_str else date.today()
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$match": {"stu.school_id": ObjectId(school_id), "date": query_date}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    result = list(Attendance.objects.aggregate(*pipeline))
    return {
        "labels": [r["_id"] for r in result],
        "data": [r["count"] for r in result]
    }

# ✅ 2. Absent/Leave List Table 
@attendanceAnalytcsModule.get("/report/attendance/status-list")
def attendance_status_list(school_id: str, date_str: str, status: str):
    query_date = datetime.fromisoformat(date_str).date()
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$match": {
            "stu.school_id": ObjectId(school_id),
            "date": query_date,
            "status": status
        }},
        {"$project": {
            "student_id": "$stu._id",
            "name": {"$concat": ["$stu.first_name", " ", "$stu.last_name"]},
            "roll_number": "$stu.roll_number",
            "class_id": "$stu.class_id",
            "section_id": "$stu.section_id"
        }}
    ]
    return list(Attendance.objects.aggregate(*pipeline))

# ✅ 3. Class-wise Attendance Trend (Line)
@attendanceAnalytcsModule.get("/report/attendance/class-trend")
def class_trend(school_id: str):
    start_date = date.today() - timedelta(days=6)
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$match": {
            "stu.school_id": ObjectId(school_id),
            "date": {"$gte": start_date}
        }},
        {"$group": {
            "_id": {"class": "$stu.class_id", "date": "$date"},
            "present": {"$sum": {"$cond": [{"$eq": ["$status", "Present"]}, 1, 0]}},
            "total": {"$sum": 1}
        }}
    ]
    raw = list(Attendance.objects.aggregate(*pipeline))
    data_by_class = {}
    labels_set = set()
    for r in raw:
        cls = str(r["_id"]["class"])
        d = r["_id"]["date"].strftime("%d %b")
        percent = round((r["present"] / r["total"]) * 100, 2) if r["total"] else 0
        data_by_class.setdefault(cls, {})[d] = percent
        labels_set.add(d)
    labels = sorted(list(labels_set))
    datasets = [{"label": cls, "data": [data_by_class[cls].get(day, 0) for day in labels]} for cls in data_by_class]
    return {"labels": labels, "datasets": datasets}

# ✅ 4. Student-wise Monthly Attendance %
@attendanceAnalytcsModule.get("/report/attendance/student-percent")
def student_percent(school_id: str, month: int, year: int, class_id: str = None):
    match = {
        "stu.school_id": ObjectId(school_id),
        "$expr": {
            "$and": [
                {"$eq": [{"$month": "$date"}, month]},
                {"$eq": [{"$year": "$date"}, year]}
            ]
        }
    }
    if class_id:
        match["stu.class_id"] = ObjectId(class_id)
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$match": match},
        {"$group": {
            "_id": "$student",
            "name": {"$first": {"$concat": ["$stu.first_name", " ", "$stu.last_name"]}},
            "present": {"$sum": {"$cond": [{"$eq": ["$status", "Present"]}, 1, 0]}},
            "total": {"$sum": 1}
        }}
    ]
    results = list(Attendance.objects.aggregate(*pipeline))
    labels = [r["name"] for r in results]
    data = [round((r["present"] / r["total"]) * 100, 2) if r["total"] else 0 for r in results]
    return {"labels": labels, "datasets": [{"label": "Attendance %", "data": data}]}

# ✅ 5. Low Attendance Alerts (< 75%)
@attendanceAnalytcsModule.get("/report/attendance/low-alerts")
def low_attendance(school_id: str, month: int, year: int, threshold: int = 75):
    response = student_percent(school_id, month, year)
    low = []
    for i in range(len(response["labels"])):
        if response["datasets"][0]["data"][i] < threshold:
            low.append({
                "name": response["labels"][i],
                "attendance_percentage": response["datasets"][0]["data"][i]
            })
    return {"students": low}

# ✅ 6. Multi-School Comparison
@attendanceAnalytcsModule.get("/report/attendance/school-compare")
def school_comparison():
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$group": {
            "_id": "$stu.school_id",
            "present": {"$sum": {"$cond": [{"$eq": ["$status", "Present"]}, 1, 0]}},
            "total": {"$sum": 1}
        }}
    ]
    result = list(Attendance.objects.aggregate(*pipeline))
    labels = [str(r["_id"]) for r in result]
    values = [round((r["present"] / r["total"]) * 100, 2) if r["total"] else 0 for r in result]
    return {"labels": labels, "datasets": [{"label": "School Attendance %", "data": values}]}

# ✅ 7. Weekly Summary (Bar)
@attendanceAnalytcsModule.get("/report/attendance/weekly-summary")
def weekly_summary(school_id: str):
    start = date.today() - timedelta(days=6)
    pipeline = [
        {"$lookup": {"from": "students", "localField": "student", "foreignField": "_id", "as": "stu"}},
        {"$unwind": "$stu"},
        {"$match": {"stu.school_id": ObjectId(school_id), "date": {"$gte": start}}},
        {"$group": {
            "_id": {"date": "$date", "status": "$status"},
            "count": {"$sum": 1}
        }}
    ]
    raw = list(Attendance.objects.aggregate(*pipeline))
    status_data = {"Present": {}, "Absent": {}, "Leave": {}}
    labels = set()
    for r in raw:
        day = r["_id"]["date"].strftime("%a")
        status_data[r["_id"]["status"]][day] = r["count"]
        labels.add(day)
    labels = sorted(list(labels))
    datasets = [{"label": status, "data": [status_data[status].get(d, 0) for d in labels]} for status in status_data]
    return {"labels": labels, "datasets": datasets}

# ✅ 8. Student Attendance History
@attendanceAnalytcsModule.get("/report/attendance/student-history")
def student_attendance(student_id: str, from_date: str = None, to_date: str = None):
    query = Q(student=ObjectId(student_id))
    if from_date:
        query &= Q(date__gte=datetime.fromisoformat(from_date).date())
    if to_date:
        query &= Q(date__lte=datetime.fromisoformat(to_date).date())

    records = Attendance.objects(query).order_by("date")
    return {
        "student_id": student_id,
        "history": [{"date": str(r.date), "status": r.status} for r in records]
    }
