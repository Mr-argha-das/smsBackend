
from typing import Optional
from pydantic import BaseModel
class BookIn(BaseModel):
    school_id: str
    title: str
    author: str
    isbn: str
    total_copies: int
    category: Optional[str] = "General"

class BookOut(BaseModel):
    id: str
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int
    category: str

class IssueIn(BaseModel):
    school_id: str
    student_id: str
    book_id: str

class ReturnIn(BaseModel):
    issue_id: str

class RenewIn(BaseModel):
    issue_id: str

class ReserveIn(BaseModel):
    school_id: str
    student_id: str
    book_id: str