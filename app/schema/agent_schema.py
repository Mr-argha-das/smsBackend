# executor/query_executor.py

def execute_mongoengine_code(code: str):
    local_env = {}

    # Import all MongoEngine app.models mentioned in your system prompt
    from app.models.announcement import Announcement
    from app.models.attendance import Attendance
    from app.models.classes import Class
    from app.models.classes import Section
    from app.models.client_app import ClientApp
    from app.models.exam_seating import Room
    from app.models.exam_seating import ExamHallSeating
    from app.models.feedback import Feedback
    from app.models.holiday import Holiday
    from app.models.hostel import Hostel
    from app.models.hostel import Block
    from app.models.hostel import HostelRoom
    from app.models.hostel import HostelAllocation
    from app.models.hostel import VisitorLog
    from app.models.hostel import StudentMovement
    from app.models.hostel import HostelAsset
    from app.models.hostel import HostelWarden
    from app.models.inventory import Category
    from app.models.inventory import Asset
    from app.models.inventory import AssetMovement
    from app.models.inventory import AssetMaintenance
    from app.models.library_models import Book
    from app.models.library_models import IssueRecord
    from app.models.library_models import Reservation
    from app.models.log import CommunicationLog
    from app.models.notification import Notification
    from app.models.period import Period
    from app.models.role import Role
    from app.models.school import School
    from app.models.student import Student
    from app.models.studentResult import StudentResult
    from app.models.subjects import Subject
    from app.models.timetable_entry import TimetableEntry
    from app.models.user import User

    # Define safe globals
    safe_globals = {
        "Announcement": Announcement,
        "Attendance": Attendance,
        "Class": Class,
        "Section": Section,
        "ClientApp": ClientApp,
        "Room": Room,
        "ExamHallSeating": ExamHallSeating,
        "Feedback": Feedback,
        "Holiday": Holiday,
        "Hostel": Hostel,
        "Block": Block,
        "HostelRoom": HostelRoom,
        "HostelAllocation": HostelAllocation,
        "VisitorLog": VisitorLog,
        "StudentMovement": StudentMovement,
        "HostelAsset": HostelAsset,
        "HostelWarden": HostelWarden,
        "Category": Category,
        "Asset": Asset,
        "AssetMovement": AssetMovement,
        "AssetMaintenance": AssetMaintenance,
        "Book": Book,
        "IssueRecord": IssueRecord,
        "Reservation": Reservation,
        "CommunicationLog": CommunicationLog,
        "Notification": Notification,
        "Period": Period,
        "Role": Role,
        "School": School,
        "Student": Student,
        "StudentResult": StudentResult,
        "Subject": Subject,
        "TimetableEntry": TimetableEntry,
        "User": User,
        "__builtins__": {},  # restrict all built-in functions for safety
    }

    try:
        # Execute GPT-generated MongoEngine code
        exec(code, safe_globals, local_env)
        result = local_env.get("result", None)

        if isinstance(result, list):
            return [r.to_mongo().to_dict() for r in result]
        elif result:
            return result.to_mongo().to_dict()

        return {"message": "Executed successfully, no result returned."}

    except Exception as e:
        return {"error": str(e)}
