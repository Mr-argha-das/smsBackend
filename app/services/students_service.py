import os
import json
import shutil
from datetime import datetime
from fastapi import HTTPException, UploadFile

from app.models.classes import Class, Section
from app.models.school import School
from app.models.student import Student


UPLOAD_DIR = "uploads/students/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def add_student_service(data: dict, image: UploadFile = None):
    school = School.objects(id=data["school_id"]).first()
    cls = Class.objects(id=data["class_id"]).first()
    sec = Section.objects(id=data["section_id"]).first()
    if not (school and cls and sec):
        raise HTTPException(status_code=404, detail="School, Class or Section not found.")

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
        first_name=data["first_name"],
        last_name=data["last_name"],
        gender=data["gender"],
        dob=data.get("dob", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        roll_number=data["roll_number"],
        address=data.get("address", ""),
        city=data.get("city", ""),
        state=data.get("state", ""),
        pincode=data.get("pincode", ""),
        guardian_name=data["guardian_name"],
        guardian_email=data.get("guardian_email", ""),
        guardian_phone=data["guardian_phone"],
        guardian_relation=data.get("guardian_relation", "Parent"),
        profile_image_url=image_url,
    )
    student.save()
    return {"message": "Student added successfully", "id": str(student.id)}


def get_all_students_service(school_id=None):
    students = Student.objects(school_id=school_id) if school_id else Student.objects()
    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
        s["school_id"] = str(s["school_id"]["$oid"])
        s["class_id"] = str(s["class_id"]["$oid"])
        s["section_id"] = str(s["section_id"]["$oid"])
    return {"data": data, "status": True}


def get_student_by_id_service(student_id: str):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    data = json.loads(student.to_json())
    data["_id"] = str(student.id)
    data["school_id"] = str(data["school_id"]["$oid"])
    data["class_id"] = str(data["class_id"]["$oid"])
    data["section_id"] = str(data["section_id"]["$oid"])
    return {"data": data, "status": True}


def update_student_service(student_id: str, payload: dict):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.update(**payload)
    return {"message": "Student updated successfully"}


def deactivate_student_service(student_id: str):
    student = Student.objects(id=student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.is_active = False
    student.save()
    return {"message": "Student deactivated"}


def get_students_by_class_service(class_id: str):
    students = Student.objects(class_id=class_id)
    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
    return {"data": data, "status": True}


def get_students_by_section_service(section_id: str):
    students = Student.objects(section_id=section_id)
    data = json.loads(students.to_json())
    for s in data:
        s["_id"] = str(s["_id"]["$oid"])
    return {"data": data, "status": True}


def login_with_otp_service(phone: str, otp: str):
    student = Student.objects(phone=phone).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if otp != "1234":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {
        "message": "Login successful",
        "student_id": str(student.id),
        "student_name": f"{student.first_name} {student.last_name}",
        "data": json.loads(student.to_json()),
        "status": True
    }
