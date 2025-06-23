from mongoengine import EmbeddedDocument, StringField, FloatField, DateTimeField

class FeeTerm(EmbeddedDocument):
    term_name = StringField(required=True)
    amount = FloatField(required=True)
    due_date = DateTimeField(required=True)
