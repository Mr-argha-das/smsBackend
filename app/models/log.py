from mongoengine import Document, ReferenceField, StringField, DateTimeField
from datetime import datetime

from app.models.user import User

class CommunicationLog(Document):
    school_id =StringField(required=True)
    sender = ReferenceField(User)
    receiver = ReferenceField(User)
    message = StringField(required=True)
    type = StringField(required=True)  # "email", "sms", "notification"
    timestamp = DateTimeField(default=datetime.utcnow)

