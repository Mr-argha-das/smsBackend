from fastapi import APIRouter
from bson import ObjectId
from app.utils.mongoRawQuery import get_inactive_students, get_monthly_admissions, get_total_students_by_class_and_gender
from app.models.student import Student

studentRouterModule = APIRouter()

@studentRouterModule.get("/students/class-gender")
def students_by_class_gender(school_id: str):
    data = get_total_students_by_class_and_gender(ObjectId(school_id))

    labels = []
    male_counts = []
    female_counts = []
    other_counts = []

    for item in data:
        class_id = str(item["_id"])
        labels.append(class_id)
        male = female = other = 0
        for g in item["gender_counts"]:
            if g["gender"] == "Male":
                male = g["count"]
            elif g["gender"] == "Female":
                female = g["count"]
            else:
                other = g["count"]
        male_counts.append(male)
        female_counts.append(female)
        other_counts.append(other)

    return {
        "labels": labels,
        "datasets": [
            {"label": "Male", "data": male_counts},
            {"label": "Female", "data": female_counts},
            {"label": "Other", "data": other_counts}
        ]
    }

@studentRouterModule.get("/students/monthly-admissions")
def monthly_admissions(school_id: str):
    data = get_monthly_admissions(ObjectId(school_id))

    labels = []
    values = []
    for d in data:
        label = f"{d['_id']['month']:02d}/{d['_id']['year']}"
        labels.append(label)
        values.append(d["count"])

    return {
        "labels": labels,
        "datasets": [
            {
                "label": "Monthly Admissions",
                "data": values
            }
        ]
    }

@studentRouterModule.get("/students/inactive")
def inactive_students(school_id: str):
    students = get_inactive_students(ObjectId(school_id))
    return {
        "count": students.count(),
        "students": [
            {
                "name": f"{s.first_name} {s.last_name}",
                "roll_number": s.roll_number,
                "class_id": str(s.class_id.id),
                "section_id": str(s.section_id.id)
            } for s in students
        ]
    }