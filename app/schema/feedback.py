from pydantic import BaseModel
from datetime import datetime

class FeedbackCreate(BaseModel):
    school_id :str
    user_id: str
    subject: str
    message: str

class FeedbackOut(FeedbackCreate):
    id: str
    status: str
    created_at: datetime
