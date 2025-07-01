from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField, ReferenceField, ListField, EmbeddedDocumentField
from datetime import datetime

from school import School
from fess import FeeTerm

class Class(Document):
    school_id = ReferenceField(School, required=True)
    class_name = StringField(required=True)
    is_active = BooleanField(default=True)
    fee_structure = ListField(EmbeddedDocumentField(FeeTerm))

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

