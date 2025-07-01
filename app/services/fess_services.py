from pyclbr import Class
import shutil
from typing import List
from fastapi import Depends, File, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

from app.models.classes import Section
from app.models.fess import FeeTerm
from app.models.fess_status import FeePaymentStatus
from app.models.school import School
from app.models.student import Student
from app.schema.auth import get_current_user
class FeeTermSchema(BaseModel):
    term_name: str
    amount: float
    due_date: datetime

class StudentCreateSchema(BaseModel):
    school_id: str
    class_id: str
    section_id: str
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

UPLOAD_DIR = "uploads/students/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# --------------------------- #
# 🔷 Fee Initializer
# --------------------------- #
def initialize_student_fees(student: Student):
    cls = student.class_id
    if not cls or not cls.fee_structure:
        return

    student.fee_status = [
        FeePaymentStatus(term_name=term.term_name, paid=False, amount_paid=0.0)
        for term in cls.fee_structure
    ]
    student.save()

# --------------------------- #
# 🔷 Sync Fee for Existing Students
# --------------------------- #
def sync_fee_terms_with_class_students(cls: Class):
    students = Student.objects(class_id=cls)
    for student in students:
        existing_terms = {fee.term_name for fee in student.fee_status}
        for term in cls.fee_structure:
            if term.term_name not in existing_terms:
                student.fee_status.append(FeePaymentStatus(term_name=term.term_name, paid=False, amount_paid=0.0))
        student.save()

def set_class_fee_structure_service(class_id: str, terms: List[FeeTermSchema]):
    cls = Class.objects(id=class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    
    cls.fee_structure = [FeeTerm(**term.dict()) for term in terms]
    cls.save()

    sync_fee_terms_with_class_students(cls)

    return {"message": f"Fee structure updated for class {cls.class_name}"}


async def add_student_service(
    school_id: str,
    class_id: str,
    section_id: str,
    first_name: str,
    last_name: str,
    gender: str,
    dob: str,
    email: str,
    phone: str,
    roll_number: str,
    address: str,
    city: str,
    state: str,
    pincode: str,
    guardian_name: str,
    guardian_email: str,
    guardian_phone: str,
    guardian_relation: str,
    image:  File(None), # type: ignore

):
    # Validate references
    school = School.objects(id=school_id).first()
    cls = Class.objects(id=class_id).first()
    sec = Section.objects(id=section_id).first()
    if not (school and cls and sec):
        raise HTTPException(status_code=404, detail="School, Class or Section not found.")

    # Save image
    image_url = ""
    if image:
        filename = f"{datetime.utcnow().timestamp()}_{image.filename.replace(' ', '_')}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/uploads/students/{filename}"

    # Save student
    student = Student(
        school_id=school,
        class_id=cls,
        section_id=sec,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        dob=dob,
        email=email,
        phone=phone,
        roll_number=roll_number,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        guardian_name=guardian_name,
        guardian_email=guardian_email,
        guardian_phone=guardian_phone,
        guardian_relation=guardian_relation,
        profile_image_url=image_url,
    )
    student.save()

    # 🔥 Add fee structure based on class
    initialize_student_fees(student)

    return {"message": "Student added successfully", "id": str(student.id)}

def pay_term_fee_service(student_id: str, term_name: str, amount: float):
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


def get_fee_status_service(student_id: str,):
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

def get_pending_students_service(school_id: str):
    students = Student.objects(school_id=school_id)
    pending_list = []
    for student in students:
        pending_terms = [fee.term_name for fee in student.fee_status if not fee.paid]
        if pending_terms:
            pending_list.append({
                "student_id": str(student.id),
                "name": f"{student.first_name} {student.last_name}",
                "pending_terms": pending_terms
            })
    return pending_list

def get_paid_students_service(school_id: str,):
    students = Student.objects(school_id=school_id)
    paid_list = []

    for student in students:
        paid_terms = [
            {
                "term_name": fee.term_name,
                "amount": fee.amount_paid,
                "paid_date": fee.paid_date
            }
            for fee in student.fee_status if fee.paid
        ]
        if paid_terms:
            paid_list.append({
                "student_id": str(student.id),
                "name": f"{student.first_name} {student.last_name}",
                "paid_terms": paid_terms
            })

    return {
        "message": "Paid students retrieved successfully",
        "data": paid_list,
        "status": True
    }