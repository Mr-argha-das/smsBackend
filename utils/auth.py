from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from adminSchools.model.table import School
from users.models.table import User

# Secret key to encode the JWT
SECRET_KEY = "xGdP7OaSl7Vw6ZgY3MfgJ8cHjOFlwChV-3EKJpBx5uY"  # use a strong, random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload  # contains sub (email), type (school/user), id, etc.


# models/client_app.py
from mongoengine import Document, StringField

class ClientApp(Document):
    client_id = StringField(required=True, unique=True)
    client_secret = StringField(required=True)
    name = StringField()

import secrets
def generate_client_credentials():
    client_id = secrets.token_hex(16)
    client_secret = secrets.token_hex(32)
    return client_id, client_secret
client_router = APIRouter()

@client_router.post("/client-init")
def create_client(ip: str = Form(...)):
    client_id, client_secret = generate_client_credentials()

    client = ClientApp(
        name=ip,
        client_id=client_id,
        client_secret=client_secret
    )
    client.save()

    return {
        "message": "Client created",
        "client_id": client_id,
        "client_secret": client_secret  # Show once only!
    }

@client_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),

):
    # Check client credentials
    client = ClientApp.objects(client_id=form_data.client_id, client_secret=form_data.client_secret).first()
    if not client:
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    email = form_data.username
    password = form_data.password

    # School Login
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

    # User Login
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

    raise HTTPException(status_code=401, detail="Invalid credentials")