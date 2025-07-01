from fastapi import APIRouter, Depends, Form, Query
from app.services.user_service import *
from app.schema.auth import get_current_user

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
    data = {
        "school_id": school_id,
        "name": name,
        "email": email,
        "phone": phone,
        "password": password,
        "subject": subject,
        "role_id": role_id
    }
    return add_user_service(data)


@user_router.get("/get-users")
def get_users(school_id: str = Query(...), current_user: dict = Depends(get_current_user)):
    return get_users_service(school_id)


@user_router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    return delete_user_service(user_id)


@user_router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    return get_profile_service(current_user)
