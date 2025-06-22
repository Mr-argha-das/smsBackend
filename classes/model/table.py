from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField, ReferenceField
from datetime import datetime

class Class(Document):
    school_id = StringField(required=True)
    class_name = StringField(required=True)
    is_active = BooleanField(default=True)

    meta = {
        "collection": "class"
    }



class Section(Document):
    class_id = ReferenceField(Class, required=True)  # 👈 ReferenceField to Class
    section_name = StringField(required=True)        # 👈 Section name (e.g., "A", "B")
    is_active = BooleanField(default=True)

    meta = {
        "collection": "section"
    }

