from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField
from datetime import datetime
from adminSchools.model.table import School
from role.model.table import Role

class User(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, unique=True)
    role = ReferenceField(Role, required=True)
    subject = StringField(required=True)
    password = StringField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "school_users"}
