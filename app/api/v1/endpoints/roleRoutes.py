import json
from fastapi import APIRouter, HTTPException, Form, Depends
from mongoengine import DoesNotExist
from app.services.role_service import add_role_service,get_role_service
from fastapi.security import OAuth2PasswordRequestForm

from app.schema.auth import get_current_user

role_router = APIRouter()

# Add a new Role with permissions
@role_router.post("/add-role")
def add_role(
    name: str = Form(...),
    permissions: list[str] = Form(...),
    school_id: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    return add_role_service(name=name, permissions=permissions, school_id=school_id)

# Get all roles
@role_router.get("/get-roles/{schoolid}")
def get_roles(schoolid:str, current_user: dict = Depends(get_current_user),):

    return get_role_service(schoolid=schoolid)