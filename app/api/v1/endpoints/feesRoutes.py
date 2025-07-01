from datetime import datetime
import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from app.services.fess_services import FeeTermSchema, get_paid_students_service, get_pending_students_service, pay_term_fee_service, set_class_fee_structure_service, add_student_service,get_fee_status_service
from app.schema.auth import get_current_user

fees_router = APIRouter()




# --------------------------- #
# 🔷 Set Fee Structure (Per Class)
# --------------------------- #
@fees_router.post("/class/{class_id}/fees")
def set_class_fee_structure(class_id: str, terms: List[FeeTermSchema], current_user: dict = Depends(get_current_user),):
    return set_class_fee_structure_service(class_id=class_id, terms=terms)



# --------------------------- #
# 🔷 Add Student (Class-wise Fee Setup)
# --------------------------- #
@fees_router.post("/add-student")
async def add_student(
    school_id: str = Form(...),
    class_id: str = Form(...),
    section_id: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: str = Form(...),
    dob: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    roll_number: str = Form(...),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    pincode: str = Form(""),
    guardian_name: str = Form(...),
    guardian_email: str = Form(""),
    guardian_phone: str = Form(...),
    guardian_relation: str = Form("Parent"),
    image: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
):
    # Validate references
    return add_student_service(school_id=school_id, class_id=class_id, section_id=section_id, first_name=first_name, last_name=last_name, gender=gender, dob=dob, email=email, phone=phone, roll_number=roll_number, address=address, city=city, state=state, pincode=pincode, guardian_name=guardian_name, guardian_email=guardian_email, guardian_phone=guardian_phone, guardian_relation=guardian_relation, image=image)

# --------------------------- #
# 🔷 Pay Fee
# --------------------------- #
@fees_router.post("/students/{student_id}/pay")
def pay_term_fee(student_id: str, term_name: str, amount: float, current_user: dict = Depends(get_current_user),):
    return pay_term_fee_service(student_id=student_id, term_name=term_name, amount=amount)

# --------------------------- #
# 🔷 Get Fee Status for Student
# --------------------------- #
@fees_router.get("/students/{student_id}/fees")
def get_fee_status(student_id: str, current_user: dict = Depends(get_current_user),):
    return get_fee_status_service(student_id=student_id)

# --------------------------- #
# 🔷 Get All Pending Students (Optional)
# --------------------------- #
@fees_router.get("/schools/{school_id}/pending")
def get_pending_students(school_id: str, current_user: dict = Depends(get_current_user),):
    return get_pending_students_service(school_id=school_id)


@fees_router.get("/schools/{school_id}/paid")
def get_paid_students(school_id: str, current_user: dict = Depends(get_current_user),):
    return get_paid_students_service(school_id=school_id)