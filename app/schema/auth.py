from datetime import timedelta
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_token
from app.models.school import School
from app.models.student import Student
from app.models.user import User
from app.models.client_app import ClientApp
import secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
client_router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


def generate_client_credentials():
    client_id = secrets.token_hex(16)
    client_secret = secrets.token_hex(32)
    return client_id, client_secret

@client_router.post("/client-init")
def create_client(ip: str = Form(...)):
    client_id, client_secret = generate_client_credentials()
    client = ClientApp(name=ip, client_id=client_id, client_secret=client_secret)
    client.save()
    return {
        "message": "Client created",
        "client_id": client_id,
        "client_secret": client_secret
    }

@client_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    client = ClientApp.objects(client_id=form_data.client_id, client_secret=form_data.client_secret).first()
    if not client:
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    email = form_data.username
    password = form_data.password

    school = School.objects(email=email, is_active=True).first()
    if school and school.phone == password:
        token = create_access_token({"sub": email, "type": "school", "id": str(school.id)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "type": "school",
            "id": str(school.id),
            "message": "School login success"
        }

    user = User.objects(email=email, password=password, is_active=True).first()
    if user:
        token = create_access_token({
            "sub": email,
            "type": "user",
            "id": str(user.id),
            "role": user.role.name
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "type": "user",
            "id": str(user.id),
            "role": user.role.name,
            "message": "User login success"
        }

    student = Student.objects(
        is_active=True,
        __raw__={
            "$or": [{"email": email}, {"guardian_email": email}],
            "$or": [{"phone": password}, {"guardian_phone": password}]
        }
    ).first()

    if student:
        token = create_access_token({
            "sub": email,
            "type": "student",
            "id": str(student.id),
            "school_id": str(student.school_id.id)
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "type": "student",
            "id": str(student.id),
            "school_id": str(student.school_id.id),
            "message": "Student login success"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")
