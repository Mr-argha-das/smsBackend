import json
from fastapi import APIRouter, HTTPException, Form, Depends, Query
from mongoengine import DoesNotExist
from users.models.table import User
from role.model.table import Role
from adminSchools.model.table import School
from fastapi.security import OAuth2PasswordRequestForm

from utils.auth import create_access_token, get_current_user, ClientApp

user_router = APIRouter()

@user_router.post("/add-user")
def add_user(
    current_user: dict = Depends(get_current_user),
    school_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    subject: str = Form(...),
    role_id: str = Form(...)
    
):
    school = School.objects(id=school_id).first()
    role = Role.objects(id=role_id).first()
    if not school or not role:
        raise HTTPException(status_code=404, detail="School or Role not found")

    if User.objects(email=email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        school_id=school,
        name=name,
        email=email,
        phone=phone,
        password=password,
        subject = subject,
        role=role
    )
    user.save()
    return {"message": "User added", "id": str(user.id)}

# Login (School or User)


@user_router.get("/get-users")
def get_users(school_id: str = Query(...),current_user: dict = Depends(get_current_user),):
    users = User.objects(school_id=school_id)
    data = json.loads(users.to_json())
    for u in data:
        u["_id"] = str(u["_id"]["$oid"])
        u["school_id"] = str(u["school_id"]["$oid"])
        u["role"] = str(u["role"]["$oid"])
    return {"data": data, "status": True}

# Delete user by id (soft delete by default)
@user_router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, current_user: dict = Depends(get_current_user),):
    user = User.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}

@user_router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "user": current_user  # contains decoded token info
    }

# Middleware for permission check (to be used inside API route)
def check_permission(role: Role, permission: str):
    if permission not in role.permissions:
        raise HTTPException(status_code=403, detail="Access denied")
