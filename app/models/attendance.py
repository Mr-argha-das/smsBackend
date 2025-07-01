from mongoengine import Document, StringField, DateField, ReferenceField
from student import Student

class Attendance(Document):
    student = ReferenceField(Student, required=True)
    date = DateField(required=True)
    status = StringField(required=True, choices=["Present", "Absent", "Leave"])
    meta = {
        "collection": "attendance"
    }