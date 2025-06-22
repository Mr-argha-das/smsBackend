import json
from fastapi import APIRouter, HTTPException, Form, Depends, Query
from mongoengine import DoesNotExist
from users.models.table import User
from role.model.table import Role
from adminSchools.model.table import School
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()

@user_router.post("/add-user")
def add_user(
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
@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    # Try school login
    school = School.objects(email=email, is_active=True).first()
    if school and school.phone == password:
        return {
            "message": "School login success",
            "id": str(school.id),
            "type": "school"
        }

    # Try user login
    user = User.objects(email=email, password=password, is_active=True).first()
    if user:
        return {
            "message": "User login success",
            "id": str(user.id),
            "type": "user",
            "role": user.role.name,

            "permissions": user.role.permissions,
            "data": json.loads(user.to_json())
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")

@user_router.get("/get-users")
def get_users(school_id: str = Query(...)):
    users = User.objects(school_id=school_id)
    data = json.loads(users.to_json())
    for u in data:
        u["_id"] = str(u["_id"]["$oid"])
        u["school_id"] = str(u["school_id"]["$oid"])
        u["role"] = str(u["role"]["$oid"])
    return {"data": data, "status": True}

# Delete user by id (soft delete by default)
@user_router.delete("/delete-user/{user_id}")
def delete_user(user_id: str):
    user = User.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}

# Middleware for permission check (to be used inside API route)
def check_permission(role: Role, permission: str):
    if permission not in role.permissions:
        raise HTTPException(status_code=403, detail="Access denied")
