from mongoengine import Document, StringField, DateField, ReferenceField, DateTimeField
from datetime import date, datetime
from .student import Student

class Attendance(Document):
    student = ReferenceField(Student, required=True)
    date = DateField(required=True, default=date.today)
    status = StringField(required=True, choices=["Present", "Absent", "Leave"])
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "attendance",
        "indexes": [
            {"fields": ("student", "date"), "unique": True}
        ]
    }