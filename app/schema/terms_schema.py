from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TermCreateSchema(BaseModel):
    school_id: str
    name: str
    academic_year: str
    start_date: datetime
    end_date: datetime
    weightage: Optional[float] = 1.0
    is_active: Optional[bool] = True

class TermUpdateSchema(BaseModel):
    name: Optional[str] = None
    academic_year: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    weightage: Optional[float] = None
    is_active: Optional[bool] = None