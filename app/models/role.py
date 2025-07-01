from mongoengine import Document, StringField, ListField

class Role(Document):
    school_id = StringField(required=True)
    name = StringField(required=True, unique=True)  # e.g., Teacher
    permissions = ListField(StringField())  # e.g., ["add-student", "get-all-students", "view-class"]

    meta = {"collection": "roles"}
