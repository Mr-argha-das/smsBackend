
from datetime import datetime
from mongoengine import Document, ReferenceField, StringField, DateTimeField,IntField

from app.models.school import School


class Hostel(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    type = StringField(choices=["Boys", "Girls", "Co-ed"], required=True)
    warden_name = StringField()
    warden_contact = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

class Block(Document):
    hostel = ReferenceField(Hostel, required=True)
    name = StringField(required=True)
    floor = IntField(default=1)
    created_at = DateTimeField(default=datetime.utcnow)

class HostelRoom(Document):
    block = ReferenceField(Block, required=True)
    room_number = StringField(required=True)
    capacity = IntField(default=1)
    type = StringField(choices=["Single", "Double", "Shared"], default="Shared")
    occupied = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)

class HostelAllocation(Document):
    student = ReferenceField("Student", required=True, unique=True)
    hostel = ReferenceField(Hostel, required=True)
    block = ReferenceField(Block)
    room = ReferenceField(HostelRoom)
    allocated_at = DateTimeField(default=datetime.utcnow)
    left_at = DateTimeField()

class VisitorLog(Document):
    student = ReferenceField("Student")
    visitor_name = StringField()
    relation = StringField()
    purpose = StringField()
    entry_time = DateTimeField(default=datetime.utcnow)
    exit_time = DateTimeField()

class StudentMovement(Document):
    student = ReferenceField("Student")
    reason = StringField()
    out_time = DateTimeField()
    in_time = DateTimeField()
    remarks = StringField()

class HostelAsset(Document):
    hostel = ReferenceField(Hostel)
    room = ReferenceField(HostelRoom, null=True)
    asset_name = StringField()
    quantity = IntField(default=1)
    condition = StringField(choices=["Working", "Damaged", "Lost"], default="Working")
    remarks = StringField()

class HostelWarden(Document):
    school_id = ReferenceField(School)
    name = StringField()
    contact = StringField()
    assigned_hostel = ReferenceField(Hostel, null=True)
    assigned_block = ReferenceField(Block, null=True)