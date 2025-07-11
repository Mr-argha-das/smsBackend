from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class SubjectResultSchema(BaseModel):
    subject: str  # Subject ID
    marks_obtained: float
    maximum_marks: float

class ResultCreateSchema(BaseModel):
    student_id: str
    student_name: str
    class_id: str
    section_id: str
    roll_number: int
    school_id: str
    academic_year: str
    subjects: List[SubjectResultSchema]
    exam_type: str
    exam_date: datetime
    result_published_date: datetime
    term_id: str  # AcademicTerm ID
    created_by: str
    performance_trend: Optional[dict] = None
    attendance_percentage: Optional[float] = None
    behavior_grade: Optional[str] = None
    co_curricular_performance: Optional[dict] = None