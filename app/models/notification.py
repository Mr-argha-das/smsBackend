from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
from datetime import datetime

from app.models.user import User
\
class Notification(Document):
    school_id = StringField(required=True)
    user = ReferenceField(User)
    content = StringField(required=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
