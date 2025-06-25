import json
from fastapi import APIRouter, Depends, HTTPException, Form
from classes.model.table import Class, Section  # path adjust karna
from bson import ObjectId

from utils.auth import get_current_user

class_section_router = APIRouter()

@class_section_router.post("/add-class")
def add_class(
    current_user: dict = Depends(get_current_user),

    class_name: str = Form(...)
    
):
    # Duplicate check
    print(current_user["id"])
    existing = Class.objects(school_id=current_user["id"], class_name=class_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class already exists for this school.")

    new_class = Class(school_id=current_user["id"], class_name=class_name)
    new_class.save()

    data = json.loads(new_class.to_json())
    data["_id"] = str(new_class.id)

    return {
        "message": "Class added successfully",
        "class_id": str(new_class.id),
        "data": data,
        "status": True
    }


@class_section_router.post("/add-section")
def add_section(
   
    class_id: str = Form(...),
    section_name: str = Form(...)
):
    cls = Class.objects(id=class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found.")

    existing = Section.objects( class_id=class_id, section_name=section_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Section already exists for this class.")

    new_section = Section( class_id=cls, section_name=section_name)
    new_section.save()

    data = json.loads(new_section.to_json())
    data["_id"] = str(new_section.id)
    data["class_id"] = str(class_id)

    return {
        "message": "Section added successfully",
        "section_id": str(new_section.id),
        "data": data,
        "status": True
    }


@class_section_router.get("/get-classes")
def get_classes(current_user: dict = Depends(get_current_user),):
    classes = Class.objects(school_id=current_user["id"])
    class_list = json.loads(classes.to_json())

    for cls in class_list:
        cls["_id"] = str(cls["_id"]["$oid"])

    return {
        "message": "Class list",
        "data": class_list,
        "status": True
    }

@class_section_router.get("/get-sections/{class_id}")
def get_sections(class_id: str):
    sections = Section.objects(class_id=class_id)
    section_list = json.loads(sections.to_json())

    for sec in section_list:
        sec["_id"] = str(sec["_id"]["$oid"])
        sec["class_id"] = str(sec["class_id"]["$oid"])  # reference to class id

    return {
        "message": "Section list",
        "data": section_list,
        "status": True
    }

@class_section_router.put("/deactivate-class/{class_id}")
def deactivate_class(class_id: str):
    cls = Class.objects(id=class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found.")
    
    cls.is_active = False
    cls.save()

    return {"message": "Class deactivated", "status": True}

@class_section_router.put("/deactivate-section/{section_id}")
def deactivate_section(section_id: str):
    section = Section.objects(id=section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found.")
    
    section.is_active = False
    section.save()

    return {"message": "Section deactivated", "status": True}


