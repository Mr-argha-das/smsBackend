from pydantic import BaseModel
from datetime import datetime

class CommunicationLogCreate(BaseModel):
    school_id :str
    sender_id: str
    receiver_id: str
    message: str
    type: str  # email, sms, notification

class CommunicationLogOut(CommunicationLogCreate):
    id: str
    timestamp: datetime