from mongoengine import EmbeddedDocument, StringField, BooleanField, FloatField, DateTimeField

class FeePaymentStatus(EmbeddedDocument):
    term_name = StringField(required=True)
    paid = BooleanField(default=False)
    paid_date = DateTimeField()
    amount_paid = FloatField(default=0.0)
