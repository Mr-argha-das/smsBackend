import json
import shutil
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi import File, HTTPException

from app.models.school import School


UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def register_school_with_image_service(
    school_name: str,
    email: str,
    phone: str,
    principal_name: str,
    address: str ,
    city: str ,
    state: str ,
    country: str ,
    pincode: str ,
    number_of_students: int = 0,
    image: UploadFile = File(...) # type: ignore
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
    school = school.School(
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


async def get_all_schools_service():
    schools_data = School.objects.all()
    print(schools_data)
    fromjson = json.loads(schools_data.to_json())
    return {
        "message": "Here is the full list of schools",
        "data": fromjson,
        "status": True
    }