from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField, EmbeddedDocumentField, ListField
from datetime import datetime
from classes.model.table import Class, Section
from adminSchools.model.table import School
from .fees_status import FeePaymentStatus
class Student(Document):
    school_id = ReferenceField(School, required=True)
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=True)

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    gender = StringField(choices=["Male", "Female", "Other"])
    dob = StringField()
    email = StringField()
    phone = StringField()

    admission_date = DateTimeField(default=datetime.utcnow)
    roll_number = StringField(required=True)

    address = StringField()
    city = StringField()
    state = StringField()
    pincode = StringField()

    # 👇 Parent/Guardian Info
    guardian_name = StringField(required=True)
    guardian_email = StringField()
    guardian_phone = StringField(required=True)
    guardian_relation = StringField(default="Parent")  # Father, Mother, Uncle, etc.

    profile_image_url = StringField()

    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    fee_status = ListField(EmbeddedDocumentField(FeePaymentStatus))

    meta = {
        "collection": "students"
    }
