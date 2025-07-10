from mongoengine import (
    Document, StringField, ReferenceField, DateTimeField,
    IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime

class Room(Document):
    school_id = StringField(required=True)
    name = StringField(required=True)
    capacity = IntField(required=True)
    room_type = StringField(choices=["Classroom", "Lab", "Hall"], default="Classroom")
    created_by = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    meta = {"collection": "rooms"}


class StudentSeat(EmbeddedDocument):
    student_id = StringField(required=True)
    roll_number = IntField(required=True)
    seat_number = StringField(required=True)


class ExamHallSeating(Document):
    school_id = StringField(required=True)
    exam_type = StringField(required=True)
    exam_date = DateTimeField(required=True)
    class_id = StringField(required=True)
    section_id = StringField()
    room_id = ReferenceField(Room, required=True)
    seats = ListField(EmbeddedDocumentField(StudentSeat))
    created_by = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    meta = {"collection": "exam_seating"}