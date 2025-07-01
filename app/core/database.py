from mongoengine import connect
from app.core.settings.dev import settings

def init_db():
    connect(
        db=settings.mongo_db_name,
        host=settings.mongo_uri,
        alias="default"
    )
