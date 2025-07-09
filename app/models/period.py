from mongoengine import Document, StringField, IntField

class Period(Document):
    name = StringField(required=True)      # e.g. "Period 1"
    start_time = StringField(required=True)  # "09:00"
    end_time = StringField(required=True)    # "09:45"
    order = IntField(required=True)        # Sorting order

    meta = {"collection": "periods"}
