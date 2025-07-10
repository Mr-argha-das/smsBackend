from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from bson import ObjectId
from app.models.student import Student
from collections import defaultdict
from datetime import datetime
from io import StringIO
import csv

feesAnalytcs = APIRouter()

# ✅ CSV Export Utility
def export_csv(data, fields):
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=fee_report.csv"
    })

# ✅ 1. Total Fee Summary (Pie Chart)
@feesAnalytcs.get("/report/fee/total-summary")
def total_fee_summary(school_id: str):
    students = Student.objects(school_id=ObjectId(school_id))
    collected = 0.0
    pending = 0.0

    for student in students:
        for term in student.fee_status:
            collected += term.amount_paid or 0
            if not term.paid:
                pending += term.amount_paid or 0

    return {
        "labels": ["Collected", "Pending"],
        "data": [collected, pending]
    }

# ✅ 2. Class-wise Pending Fee (Bar Chart)
@feesAnalytcs.get("/report/fee/class-wise")
def class_wise_pending(school_id: str):
    students = Student.objects(school_id=ObjectId(school_id))
    pending_by_class = defaultdict(float)

    for student in students:
        class_id = str(student.class_id.id) if student.class_id else "Unknown"
        for term in student.fee_status:
            if not term.paid:
                pending_by_class[class_id] += term.amount_paid or 0

    return {
        "labels": list(pending_by_class.keys()),
        "datasets": [{
            "label": "Pending Fee",
            "data": list(pending_by_class.values())
        }]
    }

# ✅ 3. Term-wise Status (Bar Chart or Table)
@feesAnalytcs.get("/report/fee/term-status")
def term_status(school_id: str):
    students = Student.objects(school_id=ObjectId(school_id))
    term_summary = defaultdict(lambda: {"paid": 0, "unpaid": 0})

    for student in students:
        for term in student.fee_status:
            if term.paid:
                term_summary[term.term_name]["paid"] += 1
            else:
                term_summary[term.term_name]["unpaid"] += 1

    labels = list(term_summary.keys())
    paid = [term_summary[t]["paid"] for t in labels]
    unpaid = [term_summary[t]["unpaid"] for t in labels]

    return {
        "labels": labels,
        "datasets": [
            {"label": "Paid", "data": paid},
            {"label": "Unpaid", "data": unpaid}
        ]
    }

# ✅ 4. Defaulters List (Table)
@feesAnalytcs.get("/report/fee/defaulters")
def defaulter_list(school_id: str, threshold: float = 0):
    students = Student.objects(school_id=ObjectId(school_id))
    defaulters = []

    for student in students:
        total_due = 0
        total_paid = 0
        for term in student.fee_status:
            total_paid += term.amount_paid or 0
            if not term.paid:
                total_due += term.amount_paid or 0
        if total_due > threshold:
            defaulters.append({
                "student_id": str(student.id),
                "name": f"{student.first_name} {student.last_name}",
                "roll_number": student.roll_number,
                "total_paid": total_paid,
                "total_due": total_due
            })

    return defaulters

# ✅ 5. Export All Fee Data (CSV)
@feesAnalytcs.get("/report/fee/export")
def export_fee_data(school_id: str):
    students = Student.objects(school_id=ObjectId(school_id))
    export_data = []

    for student in students:
        for term in student.fee_status:
            export_data.append({
                "student_name": f"{student.first_name} {student.last_name}",
                "roll_number": student.roll_number,
                "term": term.term_name,
                "paid": "Yes" if term.paid else "No",
                "amount_paid": term.amount_paid,
                "paid_date": term.paid_date.strftime("%Y-%m-%d") if term.paid_date else ""
            })

    return export_csv(export_data, [
        "student_name", "roll_number", "term", "paid", "amount_paid", "paid_date"
    ])
