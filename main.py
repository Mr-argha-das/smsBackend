from fastapi import FastAPI
from mongoengine import connect
from adminSchools.routes.school import school_router
from fastapi.middleware.cors import CORSMiddleware
from classes.routes.class_section_router import class_section_router
from students.routes.studentRoutes import student_router
from role.routes.roleRoutes import role_router
from users.routes.userRoutes import user_router
from ai.aimodel import ai_router
from fees.routes.feesRoutes import fees_router
from utils.auth import client_router
import os

app = FastAPI()

# MongoDB connect (use environment variable for connection string)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/smsTest")
connect('smsTest', host=MONGODB_URI)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images (optional, see static files note below)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
# Comment out StaticFiles for Vercel; handle static files separately
# app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(client_router, prefix="/api/auth", tags=["Auth"])
app.include_router(school_router, prefix="/api/school", tags=["School"])
app.include_router(class_section_router, prefix="/api/class-section", tags=["Class & Section"])
app.include_router(student_router, prefix="/api/student", tags=["Student Login"])
app.include_router(role_router, prefix="/api/role", tags=["User Role"])
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(fees_router, prefix="/api/fees", tags=["Fees"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI Agent"])