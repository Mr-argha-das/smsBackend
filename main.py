from fastapi import FastAPI
from mongoengine import connect
from adminSchools.routes.school import school_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from classes.routes.class_section_router import class_section_router
from students.routes.studentRoutes import student_router
from role.routes.roleRoutes import role_router
from users.routes.userRoutes import user_router
import os

app = FastAPI()

# MongoDB connect
connect('smsTest', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/smsTest")
# Allow CORS (for frontend like Flutter or React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include school router
app.include_router(school_router, prefix="/api/school", tags=["School"])
app.include_router(class_section_router, prefix="/api/class-section", tags=["Class & Section"])
app.include_router(student_router, prefix="/api/student", tags=["Student Login"])
app.include_router(role_router, prefix="/api/role", tags=["User Role"])
app.include_router(user_router, prefix="/api/user", tags=["User"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)