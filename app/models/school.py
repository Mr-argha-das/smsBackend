from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField,EmbeddedDocumentField, ListField
from datetime import datetime
from fess import FeeTerm
class School(Document):
    school_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, unique=True)
    address = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    pincode = StringField()
    principal_name = StringField(required=True)
    number_of_students = IntField(default=0)
    is_active = BooleanField(default=True)
    registered_at = DateTimeField(default=datetime.utcnow)
    image_url = StringField()  # URL or filename of uploaded image
    fee_structure = ListField(EmbeddedDocumentField(FeeTerm))

    meta = {
        "collection": "schools"
    }
