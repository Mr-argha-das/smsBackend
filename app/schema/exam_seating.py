from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StudentSeatSchema(BaseModel):
    student_id: str
    roll_number: int
    seat_number: str


class ExamSeatingCreateSchema(BaseModel):
    school_id: str
    exam_type: str
    exam_date: datetime
    class_id: str
    section_id: Optional[str]
    room_id: str
    seats: Optional[List[StudentSeatSchema]] = None
    student_list: Optional[List[dict]] = None  # used for auto seating
    created_by: str


class ExamSeatingUpdateSchema(BaseModel):
    exam_type: Optional[str]
    exam_date: Optional[datetime]
    seats: Optional[List[StudentSeatSchema]]
    section_id: Optional[str]
    room_id: Optional[str]
    updated_at: Optional[datetime]
    updated_by: Optional[str]


class RoomCreateSchema(BaseModel):
    school_id: str
    name: str
    capacity: int
    room_type: Optional[str] = "Classroom"
    created_by: Optional[str]


class RoomUpdateSchema(BaseModel):
    name: Optional[str]
    capacity: Optional[int]
    room_type: Optional[str]
    updated_by: Optional[str]