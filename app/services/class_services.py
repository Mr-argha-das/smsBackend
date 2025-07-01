import json

from fastapi import HTTPException
from app.models.classes import Class, Section
from bson import ObjectId



def add_class_service(class_name: str, school_id: str):
    print(school_id)
    existing = Class.objects(school_id=school_id, class_name=class_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class already exists for this school.")

    new_class = Class(school_id=school_id, class_name=class_name)
    new_class.save()

    data = json.loads(new_class.to_json())
    data["_id"] = str(new_class.id)

    return {
        "message": "Class added successfully",
        "class_id": str(new_class.id),
        "data": data,
        "status": True
    }

def add_section_service(classid: str, sectionname: str):
    cls = Class.objects(id=classid).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found.")

    existing = Section.objects( class_id=classid, section_name=sectionname).first()
    if existing:
        raise HTTPException(status_code=400, detail="Section already exists for this class.")

    new_section = Section( class_id=cls, section_name=sectionname)
    new_section.save()

    data = json.loads(new_section.to_json())
    data["_id"] = str(new_section.id)
    data["class_id"] = str(classid)

    return {
        "message": "Section added successfully",
        "section_id": str(new_section.id),
        "data": data,
        "status": True
    }

def get_class_service(schoolid: str):
    classes = Class.objects(school_id=schoolid)
    class_list = json.loads(classes.to_json())
    for cls in class_list:
        cls["_id"] = str(cls["_id"]["$oid"])

    return {
        "message": "Class list",
        "data": class_list,
        "status": True
    }

def get_section_service(classid:str):
    sections = Section.objects(class_id=classid)
    section_list = json.loads(sections.to_json())

    for sec in section_list:
        sec["_id"] = str(sec["_id"]["$oid"])
        sec["class_id"] = str(sec["class_id"]["$oid"])  # reference to class id

    return {
        "message": "Section list",
        "data": section_list,
        "status": True
    }

def deactivate_class_service(class_id:str):
    cls = Class.objects(id=class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found.")
    
    cls.is_active = False
    cls.save()

    return {"message": "Class deactivated", "status": True}

def deactivate_section_service(section_id:str):
    section = Section.objects(id=section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found.")
    
    section.is_active = False
    section.save()
    return {"message": "Section deactivated", "status": True}