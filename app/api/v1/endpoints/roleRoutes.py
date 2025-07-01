import json
from fastapi import APIRouter, HTTPException, Form, Depends
from mongoengine import DoesNotExist
from role.model.table import Role
from adminSchools.model.table import School
from fastapi.security import OAuth2PasswordRequestForm

from app.schema.auth import get_current_user

role_router = APIRouter()

# Add a new Role with permissions
@role_router.post("/add-role")
def add_role(
    name: str = Form(...),
    permissions: list[str] = Form(...)
    ,current_user: dict = Depends(get_current_user),
):
    if Role.objects(name=name).first():
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(name=name, permissions=permissions)
    role.save()
    return {"message": "Role created", "id": str(role.id)}

# Get all roles
@role_router.get("/get-roles")
def get_roles(current_user: dict = Depends(get_current_user),):
    roles = Role.objects.all()
    return {"data": json.loads(roles.to_json())}