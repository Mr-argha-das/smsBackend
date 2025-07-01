import json
from fastapi import APIRouter, Depends, HTTPException, Form
from bson import ObjectId
from services.class_services import add_class_service, add_section_service, get_class_service,get_section_service,deactivate_class_service, deactivate_section_service
from app.schema.auth import get_current_user

class_section_router = APIRouter()

@class_section_router.post("/add-class")
def add_class(
    current_user: dict = Depends(get_current_user),

    class_name: str = Form(...),
    school_is: str =Form(...)
    
):
    return add_class_service(class_name=class_name, school_id=school_is)
    # Duplicate check
    


@class_section_router.post("/add-section")
def add_section(
    current_user: dict = Depends(get_current_user),
    class_id: str = Form(...),
    section_name: str = Form(...)
):
    return add_section_service(classid=class_id, sectionname=section_name)


@class_section_router.get("/get-classes/{schoolid}")
def get_classes(schoolid:str, current_user: dict = Depends(get_current_user), ):
    return get_class_service(schoolid=schoolid)

@class_section_router.get("/get-sections/{class_id}")
def get_sections(class_id: str, current_user: dict = Depends(get_current_user),):
    return get_section_service(classid=class_id)

@class_section_router.put("/deactivate-class/{class_id}")
def deactivate_class(class_id: str, current_user: dict = Depends(get_current_user),):
    return deactivate_class_service(class_id=class_id)

@class_section_router.put("/deactivate-section/{section_id}")
def deactivate_section(section_id: str, current_user: dict = Depends(get_current_user),):
    return deactivate_section_service(section_id=section_id)


