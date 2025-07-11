from datetime import datetime
from mongoengine import *

from app.models.school import School

class Category(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

class Asset(Document):
    school_id = ReferenceField(School, required=True)
    category = ReferenceField(Category)
    name = StringField(required=True)
    description = StringField()
    quantity = IntField(default=1)
    location = StringField()
    assigned_to = StringField()
    condition = StringField(choices=["Working", "Damaged", "Lost"], default="Working")
    created_at = DateTimeField(default=datetime.utcnow)
    is_deleted = BooleanField(default=False)

class AssetMovement(Document):
    asset = ReferenceField(Asset)
    from_location = StringField()
    to_location = StringField()
    moved_by = StringField()
    moved_at = DateTimeField(default=datetime.utcnow)

class AssetMaintenance(Document):
    asset = ReferenceField(Asset)
    status = StringField(choices=["Pending", "Completed"], default="Pending")
    cost = IntField(default=0)
    notes = StringField()
    reported_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField()