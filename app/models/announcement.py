from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime

class Announcement(Document):
    school_id = StringField(required=True)
    title = StringField(required=True)
    message = StringField(required=True)
    audience = ListField(StringField())  # e.g., ["all", "students", "class-10"]
    created_at = DateTimeField(default=datetime.utcnow)
