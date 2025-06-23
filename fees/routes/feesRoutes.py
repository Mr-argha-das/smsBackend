from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from adminSchools.model.table import School
from fees.models.feesTable import FeeTerm
from students.model.fees_status import FeePaymentStatus
from students.model.student import Student

class FeeTermSchema(BaseModel):
    term_name: str
    amount: float
    due_date: datetime

class StudentCreateSchema(BaseModel):
    school_id: str
    first_name: str
    last_name: str
    gender: str
    dob: str
    email: str
    phone: str
    roll_number: str
    address: str
    city: str
    state: str
    pincode: str
    guardian_name: str
    guardian_email: str
    guardian_phone: str
    guardian_relation: str = "Parent"
    profile_image_url: str = None



def initialize_student_fees(student: Student, school: School):
    student.fee_status = [
        FeePaymentStatus(term_name=term.term_name, paid=False, amount_paid=0.0)
        for term in school.fee_structure
    ]
    student.save()

def sync_fee_terms_with_students(school_id):
    school = School.objects(id=school_id).first()
    students = Student.objects(school_id=school)
    for student in students:
        existing_terms = {fee.term_name for fee in student.fee_status}
        for term in school.fee_structure:
            if term.term_name not in existing_terms:
                student.fee_status.append(FeePaymentStatus(term_name=term.term_name, paid=False, amount_paid=0.0))
        student.save()

fees_router = APIRouter()


@fees_router.post("/schools/{school_id}/fees")
def set_school_fee_structure(school_id: str, terms: List[FeeTermSchema]):
    school = School.objects(id=school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    school.fee_structure = [FeeTerm(**term.dict()) for term in terms]
    school.save()
    sync_fee_terms_with_students(school_id)
    return {"message": "Fee structure updated"}

@fees_router.post("/students/")
def add_student(data: StudentCreateSchema):
    school = School.objects(id=data.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    student = Student(**data.dict())
    student.school_id = school
    student.save()
    initialize_student_fees(student, school)
    return {"student_id": str(student.id)}

@fees_router.post("/students/{student_id}/pay")
def pay_term_fee(student_id: str, term_name: str, amount: float):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for fee in student.fee_status:
        if fee.term_name == term_name:
            if fee.paid:
                raise HTTPException(status_code=400, detail="Already paid")
            fee.paid = True
            fee.paid_date = datetime.utcnow()
            fee.amount_paid = amount
            student.save()
            return {"message": f"Paid for {term_name}"}
    raise HTTPException(status_code=404, detail="Term not found")

@fees_router.get("/students/{student_id}/fees")
def get_fee_status(student_id: str):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": f"{student.first_name} {student.last_name}",
        "fees": [
            {
                "term": fee.term_name,
                "paid": fee.paid,
                "amount": fee.amount_paid,
                "paid_date": fee.paid_date
            } for fee in student.fee_status
        ]
    }

@fees_router.get("/schools/{school_id}/pending")
def get_pending_students(school_id: str):
    students = Student.objects(school_id=school_id)
    pending_list = []
    for student in students:
        pending_terms = [fee.term_name for fee in student.fee_status if not fee.paid]
        if pending_terms:
            pending_list.fees_routerend({
                "student_id": str(student.id),
                "name": f"{student.first_name} {student.last_name}",
                "pending_terms": pending_terms
            })
    return pending_list
