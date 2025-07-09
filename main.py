from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.settings.dev import settings  # or dynamic based on ENV
from app.core.database import init_db
from app.core.middleware import HostValidationMiddleware

# Routers
from app.api.v1.endpoints.aiRoutes import agent_router
from app.api.v1.endpoints.class_section_router import class_section_router
from app.api.v1.endpoints.feesRoutes import fees_router
from app.api.v1.endpoints.roleRoutes import role_router
from app.api.v1.endpoints.schoolRoutes import school_router
from app.api.v1.endpoints.studentRoutes import student_router
from app.api.v1.endpoints.userRoutes import user_router
from app.schema.auth import client_router
from app.api.v1.endpoints.attendance import attendanceRouter

import os
import uvicorn

app = FastAPI(title=settings.app_name)
init_db()

app.add_middleware(HostValidationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(client_router, prefix="/api/auth", tags=["Auth"])
app.include_router(school_router, prefix="/api/school", tags=["School"])
app.include_router(class_section_router, prefix="/api/class-section", tags=["Class & Section"])
app.include_router(student_router, prefix="/api/student", tags=["Student Login"])
app.include_router(role_router, prefix="/api/role", tags=["User Role"])
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(fees_router, prefix="/api/fees", tags=["Fees"])
app.include_router(attendanceRouter, prefix="/api/attendance", tags=["Attendance"])
app.include_router(agent_router, prefix="/api/ai", tags=["AI"])


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=settings.debug)
