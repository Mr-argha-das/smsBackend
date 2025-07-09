from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime

from app.models.user import User


class Feedback(Document):
    school_id = StringField(required=True)
    sender = ReferenceField(User)
    subject = StringField(required=True)
    message = StringField(required=True)
    status = StringField(default="open")  # open, in_progress, resolved
    created_at = DateTimeField(default=datetime.utcnow)
