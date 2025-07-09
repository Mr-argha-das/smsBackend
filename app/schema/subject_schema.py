from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SubjectCreate(BaseModel):
    school_id: str
    class_id: str
    section_id: Optional[str]
    subject_name: str
    subject_code: Optional[str]
    assigned_teachers: Optional[List[str]] = []
    syllabus: Optional[str] = None

class SubjectUpdate(BaseModel):
    subject_name: Optional[str]
    subject_code: Optional[str]
    assigned_teachers: Optional[List[str]]
    syllabus: Optional[str]
    is_active: Optional[bool]

class SubjectResponse(SubjectCreate):
    id: str
    created_at: datetime
    updated_at: datetime
