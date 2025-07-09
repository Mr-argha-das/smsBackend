from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class SubjectMarkSchema(BaseModel):
    subject: str  # Subject ID
    marks_obtained: float
    maximum_marks: float
    grade: Optional[str] = None


class ResultCreateSchema(BaseModel):
    student_id: str
    student_name: str
    class_id: str
    section_id: Optional[str]
    roll_number: int
    school_id: str
    academic_year: str
    subjects: List[SubjectMarkSchema]

    exam_type: str
    exam_date: datetime
    result_published_date: datetime
    term_id: Optional[str]

    created_by: str

    # Optional
    performance_trend: Optional[Dict[str, float]]
    attendance_percentage: Optional[float]
    behavior_grade: Optional[str]
    co_curricular_performance: Optional[Dict[str, str]]
