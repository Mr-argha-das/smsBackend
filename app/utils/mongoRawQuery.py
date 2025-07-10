from app.models.student import Student
from mongoengine.queryset.visitor import Q

def get_total_students_by_class_and_gender(school_id):
    pipeline = [
        {"$match": {"school_id": school_id}},
        {
            "$group": {
                "_id": {"class": "$class_id", "gender": "$gender"},
                "count": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": "$_id.class",
                "gender_counts": {
                    "$push": {
                        "gender": "$_id.gender",
                        "count": "$count"
                    }
                },
                "total": {"$sum": "$count"}
            }
        }
    ]
    return list(Student.objects.aggregate(*pipeline))


from datetime import datetime
from pymongo import ASCENDING

def get_monthly_admissions(school_id):
    pipeline = [
        {"$match": {"school_id": school_id}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$admission_date"},
                    "month": {"$month": "$admission_date"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.year": ASCENDING, "_id.month": ASCENDING}}
    ]
    return list(Student.objects.aggregate(*pipeline))

def get_inactive_students(school_id):
    return Student.objects(school_id=school_id, is_active=False)
