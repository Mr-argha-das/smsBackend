import json

from fastapi import HTTPException

from app.models.role import Role

def add_role_service(
    name: str,
    school_id: str,
    permissions: list[str]
    
):
    if Role.objects(name=name).first():
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(name=name, permissions=permissions, school_id=school_id)
    role.save()
    return {"message": "Role created", "id": str(role.id)}

def get_role_service(schoolid:str):
    roles = Role.objects(school_id=schoolid).all()
    return {
        "data": json.loads(roles.to_json())
    }