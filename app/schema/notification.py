from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    school_id :str
    user_id: str
    content: str

class NotificationOut(NotificationCreate):
    id: str
    is_read: bool
    created_at: datetime