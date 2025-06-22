import os
import shutil
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from students.model.student import Student
from adminSchools.model.table import School
from classes.model.table import Class, Section

student_router = APIRouter()
UPLOAD_DIR = "uploads/students/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Add Student
@student_router.post("/add-student")
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
    image: UploadFile = File(None)
):
    # Validate references
    school = School.objects(id=school_id).first()
    cls = Class.objects(id=class_id).first()
    sec = Section.objects(id=section_id).first()
    if not (school and cls and sec):
        raise HTTPException(status_code=404, detail="School, Class or Section not found.")

    # Handle image
    image_url = ""
    if image:
        filename = f"{datetime.utcnow().timestamp()}_{image.filename.replace(' ', '_')}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/uploads/students/{filename}"

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
    return {"message": "Student added successfully", "id": str(student.id)}

# Get All Students with optional school_id filter
@student_router.get("/get-all-students")
def get_all_students(school_id: str = Query(None)):
    if school_id:
        students = Student.objects(school_id=school_id)
    else:
        students = Student.objects()

    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
        s["school_id"] = str(s["school_id"]["$oid"])
        s["class_id"] = str(s["class_id"]["$oid"])
        s["section_id"] = str(s["section_id"]["$oid"])
    return {"data": data, "status": True}

# Get Student By ID
@student_router.get("/get-student/{student_id}")
def get_student(student_id: str):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    data = json.loads(student.to_json())
    data["_id"] = str(student.id)
    data["school_id"] = str(data["school_id"]["$oid"])
    data["class_id"] = str(data["class_id"]["$oid"])
    data["section_id"] = str(data["section_id"]["$oid"])
    return {"data": data, "status": True}

# Update Student
@student_router.put("/update-student/{student_id}")
def update_student(student_id: str, payload: dict):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.update(**payload)
    return {"message": "Student updated successfully"}

# Deactivate Student
@student_router.put("/deactivate-student/{student_id}")
def deactivate_student(student_id: str):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.is_active = False
    student.save()
    return {"message": "Student deactivated"}

# Get Students by Class
@student_router.get("/get-students-by-class/{class_id}")
def get_students_by_class(class_id: str):
    students = Student.objects(class_id=class_id)
    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
    return {"data": data, "status": True}

# Get Students by Section
@student_router.get("/get-students-by-section/{section_id}")
def get_students_by_section(section_id: str):
    students = Student.objects(section_id=section_id)
    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
    return {"data": data, "status": True}

# Student Login with static OTP
@student_router.post("/login")
def login_with_otp(phone: str = Form(...), otp: str = Form(...)):
    student = Student.objects(phone=phone).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Static OTP check for now
    if otp != "1234":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {
        "message": "Login successful",
        "student_id": str(student.id),
        "student_name": f"{student.first_name} {student.last_name}",
        "data": json.loads(student.to_josn()),
        "status": True
    }
