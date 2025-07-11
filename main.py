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
from app.api.v1.endpoints.attendance import attendanceRouter
from app.api.v1.endpoints.subjects_routes import subject_router
from app.api.v1.endpoints.communication_notification_Routes import communication_router
from app.api.v1.endpoints.student_result import result_router
from app.api.v1.endpoints.timetable_routes import timeTableRoutes
from app.api.v1.endpoints.room_routes import room_router
from app.api.v1.endpoints.studentAnalyticsModule import studentRouterModule
from app.api.v1.endpoints.academicPerformanceAnalyticsModule import academicPerformanceAnalyticsModule
from app.api.v1.endpoints.attendance_report_router import attendanceAnalytcsModule
from app.api.v1.endpoints.feeCollectionAnalytics import feesAnalytcs
from app.api.v1.endpoints.book_routes import booksRouter
from app.api.v1.endpoints.inventroy_routes import inventoryRouter
from app.api.v1.endpoints.hostel_routes import hostelRouter
from app.schema.auth import client_router

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
app.include_router(subject_router, prefix="/api/subject", tags=["subject"])
app.include_router(result_router, prefix="/api/exam", tags=["Exams / Result"])
app.include_router(room_router, prefix="/api/room", tags=["Examination Hall & Seating plan"])
app.include_router(timeTableRoutes, prefix="/api/timetable", tags=["Time Table"])
app.include_router(role_router, prefix="/api/role", tags=["User Role"])
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(fees_router, prefix="/api/fees", tags=["Fees"])
app.include_router(attendanceRouter, prefix="/api/attendance", tags=["Attendance"])
app.include_router(studentRouterModule, prefix="/api/report/students", tags=["Student Analytics Module"])
app.include_router(academicPerformanceAnalyticsModule, prefix="/api/academic-performance", tags=["Academic Performance Analytics Module"])
app.include_router(attendanceAnalytcsModule, prefix="/api/attendance-analytcs", tags=["Attendance Analytics Module"])
app.include_router(feesAnalytcs, prefix="/api/feesAnalytcs", tags=["Fee Collection Analytics"])
app.include_router(booksRouter, prefix="/api/librray", tags=["Librray Managment module"])
app.include_router(inventoryRouter, prefix="/api/inventory", tags=["Inventory Managment "])
app.include_router(communication_router, prefix="/api/Communication",tags=["Communication"])
app.include_router(hostelRouter, prefix="/api/hostel", tags=["Hostel Management"])

app.include_router(agent_router, prefix="/api/ai", tags=["AI"])




if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=settings.debug)
