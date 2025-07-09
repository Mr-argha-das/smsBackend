from mongoengine import Document, ReferenceField, StringField, DateTimeField
from datetime import datetime
from .classes import Class, Section
from .user import User
from .subjects import Subject
from .period import Period

class TimetableEntry(Document):
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=True)
    subject_id = ReferenceField(Subject, required=True)
    teacher_id = ReferenceField(User, required=True)
    period_id = ReferenceField(Period, required=True)
    room = StringField(required=False)
    day = StringField(required=True)  # Monday, Tuesday, ...

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "timetable"}
