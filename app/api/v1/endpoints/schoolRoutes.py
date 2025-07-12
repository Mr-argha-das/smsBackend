import json
import shutil
import os
from app.models.school import School
from app.services.school_services import get_all_schools_service, register_school_with_image_service
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
school_router = APIRouter()

@school_router.post("/register-school")
async def register_school_with_image(
    school_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    principal_name: str = Form(...),
    address: str = Form(""),
    city: str = Form(""),
    state: str = Form(""),
    country: str = Form(""),
    pincode: str = Form(""),
    number_of_students: int = Form(0),
    image: UploadFile = File(...)
):
    # Duplicate checks
    if School.objects(email=email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")
    if School.objects(phone=phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered.")

    # File extension check (optional safety)
    if not image.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        raise HTTPException(status_code=400, detail="Only image files are allowed (.jpg, .png, .webp)")

    # Save image to uploads
    filename = f"{datetime.utcnow().timestamp()}_{image.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Save to DB
    school = School(
        school_name=school_name,
        email=email,
        phone=phone,
        principal_name=principal_name,
        address=address,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
        number_of_students=number_of_students,
        image_url=file_path
    )
    school.save()

    fromjson = json.loads(school.to_json())

    return {
        "message": "School registered successfully",
        "school_id": str(school.id),
        "data": fromjson,
        "status": True
    }



@school_router.get("/get-all-schools")
async def get_all_schools():
    schools_data = School.objects.all()
    print(schools_data)
    fromjson = json.loads(schools_data.to_json())
    return {
        "message": "Here is the full list of schools",
        "data": fromjson,
        "status": True
    }
