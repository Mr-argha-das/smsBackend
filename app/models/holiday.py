from mongoengine import Document, DateField, StringField

class Holiday(Document):
    schoolId = StringField(required=True)
    date = DateField(required=True, unique=True)
    reason = StringField(required=True)

    meta = {
        "collection": "holidays"
    }