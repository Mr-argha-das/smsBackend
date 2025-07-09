from pydantic import BaseModel
from typing import Optional

class TimetableCreate(BaseModel):
    class_id: str
    section_id: str
    subject_id: str
    teacher_id: str
    period_id: str
    room: Optional[str]
    day: str

class TimetableOut(TimetableCreate):
    id: str

from pydantic import BaseModel
from typing import Optional

class TimetableUpdate(BaseModel):
    teacher_id: Optional[str]
    subject_id: Optional[str]
    period_id: Optional[str]
    room: Optional[str]
    day: Optional[str]
