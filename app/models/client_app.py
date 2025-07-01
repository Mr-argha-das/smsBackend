from mongoengine import Document, StringField

class ClientApp(Document):
    client_id = StringField(required=True, unique=True)
    client_secret = StringField(required=True)
    name = StringField()
