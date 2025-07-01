from fastapi import APIRouter, Depends, Form, File, UploadFile, Query
from app.services.students_service import *
from app.schema.auth import get_current_user

student_router = APIRouter()


@student_router.post("/add-student")
async def add_student(
    current_user: dict = Depends(get_current_user),
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
    image: UploadFile = File(None)
):
    data = locals()
    del data["current_user"]
    return await add_student_service(data, image)


@student_router.get("/get-all-students")
def get_all_students(school_id: str = Query(None), current_user: dict = Depends(get_current_user)):
    return get_all_students_service(school_id)


@student_router.get("/get-student/{student_id}")
def get_student(student_id: str, current_user: dict = Depends(get_current_user)):
    return get_student_by_id_service(student_id)


@student_router.put("/update-student/{student_id}")
def update_student(student_id: str, payload: dict, current_user: dict = Depends(get_current_user)):
    return update_student_service(student_id, payload)


@student_router.put("/deactivate-student/{student_id}")
def deactivate_student(student_id: str, current_user: dict = Depends(get_current_user)):
    return deactivate_student_service(student_id)


@student_router.get("/get-students-by-class/{class_id}")
def get_students_by_class(class_id: str, current_user: dict = Depends(get_current_user)):
    return get_students_by_class_service(class_id)


@student_router.get("/get-students-by-section/{section_id}")
def get_students_by_section(section_id: str, current_user: dict = Depends(get_current_user)):
    return get_students_by_section_service(section_id)


@student_router.post("/login")
def login_with_otp(phone: str = Form(...), otp: str = Form(...)):
    return login_with_otp_service(phone, otp)
