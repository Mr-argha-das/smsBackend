from pydantic import BaseModel
from typing import List
from datetime import datetime

class AnnouncementCreate(BaseModel):
    school_id :str
    title: str
    message: str
    audience: List[str]

class AnnouncementOut(AnnouncementCreate):
    id: str
    created_at: datetime
