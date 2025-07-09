from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField, ListField
from datetime import datetime

from .classes import Class, Section  # Assuming your file is class_model.py
from .school import School
from .user import User  # You need to create a Teacher model if not already present

class Subject(Document):
    school_id = ReferenceField(School, required=True)
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=False)  # Optional: if subject is section-specific
    subject_name = StringField(required=True)
    subject_code = StringField(required=False)
    assigned_teachers = ListField(ReferenceField(User))  # One or many teachers
    syllabus = StringField()  # Optional: store text or URL to a file
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "subject"
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
