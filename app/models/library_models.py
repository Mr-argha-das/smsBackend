from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime
from app.models.student import Student
from app.models.school import School

class Book(Document):
    school_id = ReferenceField(School)
    title = StringField()
    author = StringField()
    isbn = StringField()
    total_copies = IntField()
    available_copies = IntField()
    category = StringField()
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

class IssueRecord(Document):
    school_id = ReferenceField(School)
    student = ReferenceField(Student)
    book = ReferenceField(Book)
    issue_date = DateTimeField(default=datetime.utcnow)
    due_date = DateTimeField()
    return_date = DateTimeField()
    is_returned = BooleanField(default=False)
    fine_paid = BooleanField(default=False)

class Reservation(Document):
    school_id = ReferenceField(School)
    student = ReferenceField(Student)
    book = ReferenceField(Book)
    reserved_at = DateTimeField(default=datetime.utcnow)