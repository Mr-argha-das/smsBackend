import json
import shutil
import os
from app.services.school_services import get_all_schools_service, register_school_with_image_service
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form


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
    return register_school_with_image_service(school_name=school_name, email=email, phone=phone,principal_name=principal_name,address=address, city=city, state=state, country=country, pincode=pincode, number_of_students=number_of_students, image=image )


@school_router.get("/get-all-schools")
async def get_all_schools():
    return get_all_schools_service()
