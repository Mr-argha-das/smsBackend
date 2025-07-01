import json
from fastapi import HTTPException

from app.models.role import Role
from app.models.school import School
from app.models.user import User



def add_user_service(data: dict):
    school = School.objects(id=data["school_id"]).first()
    role = Role.objects(id=data["role_id"]).first()

    if not school or not role:
        raise HTTPException(status_code=404, detail="School or Role not found")

    if User.objects(email=data["email"]).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        school_id=school,
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        password=data["password"],
        subject=data["subject"],
        role=role
    )
    user.save()
    return {"message": "User added", "id": str(user.id)}


def get_users_service(school_id: str):
    users = User.objects(school_id=school_id)
    data = json.loads(users.to_json())
    for u in data:
        u["_id"] = str(u["_id"]["$oid"])
        u["school_id"] = str(u["school_id"]["$oid"])
        u["role"] = str(u["role"]["$oid"])
    return {"data": data, "status": True}


def delete_user_service(user_id: str):
    user = User.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}


def get_profile_service(current_user: dict):
    return {"user": current_user}


def check_permission(role: Role, permission: str):
    if permission not in role.permissions:
        raise HTTPException(status_code=403, detail="Access denied")
