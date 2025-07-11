from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime

class Announcement(Document):
    school_id = StringField(required=True)
    title = StringField(required=True)
    message = StringField(required=True)
    audience = ListField(StringField())  # e.g., ["all", "students", "class-10"]
    created_at = DateTimeField(default=datetime.utcnow)

from mongoengine import Document, StringField, DateField, ReferenceField, DateTimeField
from datetime import date, datetime
from .student import Student

class Attendance(Document):
    student = ReferenceField(Student, required=True)
    date = DateField(required=True, default=date.today)
    status = StringField(required=True, choices=["Present", "Absent", "Leave"])
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "attendance",
        "indexes": [
            {"fields": ("student", "date"), "unique": True}
        ]
    }
from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField, ReferenceField, ListField, EmbeddedDocumentField
from datetime import datetime

from .school import School
from .fess import FeeTerm

class Class(Document):
    school_id = ReferenceField(School, required=True)
    class_name = StringField(required=True)
    is_active = BooleanField(default=True)
    fee_structure = ListField(EmbeddedDocumentField(FeeTerm))

    meta = {
        "collection": "class"
    }



class Section(Document):
    class_id = ReferenceField(Class, required=True)  # 👈 ReferenceField to Class
    section_name = StringField(required=True)        # 👈 Section name (e.g., "A", "B")
    is_active = BooleanField(default=True)

    meta = {
        "collection": "section"
    }


from mongoengine import Document, StringField

class ClientApp(Document):
    client_id = StringField(required=True, unique=True)
    client_secret = StringField(required=True)
    name = StringField()

from mongoengine import (
    Document, StringField, ReferenceField, DateTimeField,
    IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime

class Room(Document):
    school_id = StringField(required=True)
    name = StringField(required=True)
    capacity = IntField(required=True)
    room_type = StringField(choices=["Classroom", "Lab", "Hall"], default="Classroom")
    created_by = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    meta = {"collection": "rooms"}


class StudentSeat(EmbeddedDocument):
    student_id = StringField(required=True)
    roll_number = IntField(required=True)
    seat_number = StringField(required=True)


class ExamHallSeating(Document):
    school_id = StringField(required=True)
    exam_type = StringField(required=True)
    exam_date = DateTimeField(required=True)
    class_id = StringField(required=True)
    section_id = StringField()
    room_id = ReferenceField(Room, required=True)
    seats = ListField(EmbeddedDocumentField(StudentSeat))
    created_by = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    meta = {"collection": "exam_seating"}
from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime

from app.models.user import User


class Feedback(Document):
    school_id = StringField(required=True)
    sender = ReferenceField(User)
    subject = StringField(required=True)
    message = StringField(required=True)
    status = StringField(default="open")  # open, in_progress, resolved
    created_at = DateTimeField(default=datetime.utcnow)

from mongoengine import EmbeddedDocument, StringField, BooleanField, FloatField, DateTimeField

class FeePaymentStatus(EmbeddedDocument):
    term_name = StringField(required=True)
    paid = BooleanField(default=False)
    paid_date = DateTimeField()
    amount_paid = FloatField(default=0.0)

from mongoengine import EmbeddedDocument, StringField, FloatField, DateTimeField

class FeeTerm(EmbeddedDocument):
    term_name = StringField(required=True)
    amount = FloatField(required=True)
    due_date = DateTimeField(required=True)

from mongoengine import Document, DateField, StringField

class Holiday(Document):
    schoolId = StringField(required=True)
    date = DateField(required=True, unique=True)
    reason = StringField(required=True)

    meta = {
        "collection": "holidays"
    }

from datetime import datetime
from mongoengine import Document, ReferenceField, StringField, DateTimeField,IntField

from app.models.school import School


class Hostel(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    type = StringField(choices=["Boys", "Girls", "Co-ed"], required=True)
    warden_name = StringField()
    warden_contact = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

class Block(Document):
    hostel = ReferenceField(Hostel, required=True)
    name = StringField(required=True)
    floor = IntField(default=1)
    created_at = DateTimeField(default=datetime.utcnow)

class HostelRoom(Document):
    block = ReferenceField(Block, required=True)
    room_number = StringField(required=True)
    capacity = IntField(default=1)
    type = StringField(choices=["Single", "Double", "Shared"], default="Shared")
    occupied = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)

class HostelAllocation(Document):
    student = ReferenceField("Student", required=True, unique=True)
    hostel = ReferenceField(Hostel, required=True)
    block = ReferenceField(Block)
    room = ReferenceField(HostelRoom)
    allocated_at = DateTimeField(default=datetime.utcnow)
    left_at = DateTimeField()

class VisitorLog(Document):
    student = ReferenceField("Student")
    visitor_name = StringField()
    relation = StringField()
    purpose = StringField()
    entry_time = DateTimeField(default=datetime.utcnow)
    exit_time = DateTimeField()

class StudentMovement(Document):
    student = ReferenceField("Student")
    reason = StringField()
    out_time = DateTimeField()
    in_time = DateTimeField()
    remarks = StringField()

class HostelAsset(Document):
    hostel = ReferenceField(Hostel)
    room = ReferenceField(HostelRoom, null=True)
    asset_name = StringField()
    quantity = IntField(default=1)
    condition = StringField(choices=["Working", "Damaged", "Lost"], default="Working")
    remarks = StringField()

class HostelWarden(Document):
    school_id = ReferenceField(School)
    name = StringField()
    contact = StringField()
    assigned_hostel = ReferenceField(Hostel, null=True)
    assigned_block = ReferenceField(Block, null=True)
from datetime import datetime
from mongoengine import *

from app.models.school import School

class Category(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

class Asset(Document):
    school_id = ReferenceField(School, required=True)
    category = ReferenceField(Category)
    name = StringField(required=True)
    description = StringField()
    quantity = IntField(default=1)
    location = StringField()
    assigned_to = StringField()
    condition = StringField(choices=["Working", "Damaged", "Lost"], default="Working")
    created_at = DateTimeField(default=datetime.utcnow)
    is_deleted = BooleanField(default=False)

class AssetMovement(Document):
    asset = ReferenceField(Asset)
    from_location = StringField()
    to_location = StringField()
    moved_by = StringField()
    moved_at = DateTimeField(default=datetime.utcnow)

class AssetMaintenance(Document):
    asset = ReferenceField(Asset)
    status = StringField(choices=["Pending", "Completed"], default="Pending")
    cost = IntField(default=0)
    notes = StringField()
    reported_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField()
from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime
from app.models.student import Student
from app.models.school import School

class Book(Document):
    school_id = ReferenceField(School)
    title = StringField()
    author = StringField()
    isbn = StringField()
    total_copies = IntField()
    available_copies = IntField()
    category = StringField()
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

class IssueRecord(Document):
    school_id = ReferenceField(School)
    student = ReferenceField(Student)
    book = ReferenceField(Book)
    issue_date = DateTimeField(default=datetime.utcnow)
    due_date = DateTimeField()
    return_date = DateTimeField()
    is_returned = BooleanField(default=False)
    fine_paid = BooleanField(default=False)

class Reservation(Document):
    school_id = ReferenceField(School)
    student = ReferenceField(Student)
    book = ReferenceField(Book)
    reserved_at = DateTimeField(default=datetime.utcnow)
from mongoengine import Document, ReferenceField, StringField, DateTimeField
from datetime import datetime

from app.models.user import User

class CommunicationLog(Document):
    school_id =StringField(required=True)
    sender = ReferenceField(User)
    receiver = ReferenceField(User)
    message = StringField(required=True)
    type = StringField(required=True)  # "email", "sms", "notification"
    timestamp = DateTimeField(default=datetime.utcnow)


from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField
from datetime import datetime

from app.models.user import User
\
class Notification(Document):
    school_id = StringField(required=True)
    user = ReferenceField(User)
    content = StringField(required=True)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

from mongoengine import Document, StringField, IntField

class Period(Document):
    name = StringField(required=True)      # e.g. "Period 1"
    start_time = StringField(required=True)  # "09:00"
    end_time = StringField(required=True)    # "09:45"
    order = IntField(required=True)        # Sorting order

    meta = {"collection": "periods"}

from mongoengine import Document, StringField, ListField

class Role(Document):
    school_id = StringField(required=True)
    name = StringField(required=True, unique=True)  # e.g., Teacher
    permissions = ListField(StringField())  # e.g., ["add-student", "get-all-students", "view-class"]

    meta = {"collection": "roles"}

from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField,EmbeddedDocumentField, ListField
from datetime import datetime
from .fess import FeeTerm
class School(Document):
    school_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, unique=True)
    address = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    pincode = StringField()
    principal_name = StringField(required=True)
    number_of_students = IntField(default=0)
    is_active = BooleanField(default=True)
    registered_at = DateTimeField(default=datetime.utcnow)
    image_url = StringField()  # URL or filename of uploaded image
    fee_structure = ListField(EmbeddedDocumentField(FeeTerm))

    meta = {
        "collection": "schools"
    }

from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField, EmbeddedDocumentField, ListField
from datetime import datetime
from .classes import Class, Section
from .school import School
from .fess_status import FeePaymentStatus


class Student(Document):
    school_id = ReferenceField(School, required=True)
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=True)

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    gender = StringField(choices=["Male", "Female", "Other"])
    dob = StringField()
    email = StringField()
    phone = StringField()

    admission_date = DateTimeField(default=datetime.utcnow)
    roll_number = StringField(required=True)

    address = StringField()
    city = StringField()
    state = StringField()
    pincode = StringField()

    # 👇 Parent/Guardian Info
    guardian_name = StringField(required=True)
    guardian_email = StringField()
    guardian_phone = StringField(required=True)
    guardian_relation = StringField(default="Parent")  # Father, Mother, Uncle, etc.

    profile_image_url = StringField()

    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    fee_status = ListField(EmbeddedDocumentField(FeePaymentStatus))

    meta = {
        "collection": "students"
    }

from mongoengine import (
    Document, StringField, ReferenceField, DateTimeField,
    ListField, EmbeddedDocument, EmbeddedDocumentField,
    FloatField, IntField, DictField
)
from datetime import datetime
from .school import School
from .classes import Class, Section
from .user import User
from .subjects import Subject


# Subject-wise marks structure
class SubjectMark(EmbeddedDocument):
    subject = ReferenceField(Subject, required=True)
    marks_obtained = FloatField(required=True)
    maximum_marks = FloatField(required=True)
    grade = StringField()


# Main result document
class StudentResult(Document):

    student_name = StringField(required=True)
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section)
    roll_number = IntField(required=True)
    school_id = ReferenceField(School, required=True)
    academic_year = StringField(required=True)

    subjects = ListField(EmbeddedDocumentField(SubjectMark))

    total_marks_obtained = FloatField()
    total_maximum_marks = FloatField()
    percentage = FloatField()
    overall_grade = StringField()
    rank_in_class = IntField()
    result_status = StringField(choices=["Pass", "Fail", "Promoted", "Detained"])

    exam_type = StringField(required=True)  # e.g., Term 1, Annual
    exam_date = DateTimeField()
    result_published_date = DateTimeField()
    term_id = StringField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    created_by = StringField()  # e.g. teacher email or user ID

    # Optional AI/Advanced fields
    performance_trend = DictField()  # {"Term 1": 80.5, "Term 2": 82.3}
    attendance_percentage = FloatField()
    behavior_grade = StringField()
    co_curricular_performance = DictField()  # {"sports": "...", "arts": "..."}

    meta = {
        "collection": "student_result"
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField, ListField
from datetime import datetime

from .classes import Class, Section  # Assuming your file is class_model.py
from .school import School
from .user import User  # You need to create a Teacher model if not already present

class Subject(Document):
    school_id = ReferenceField(School, required=True)
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=False)  # Optional: if subject is section-specific
    subject_name = StringField(required=True)
    subject_code = StringField(required=False)
    assigned_teachers = ListField(ReferenceField(User))  # One or many teachers
    syllabus = StringField()  # Optional: store text or URL to a file
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "subject"
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

from mongoengine import Document, ReferenceField, StringField, DateTimeField
from datetime import datetime
from .classes import Class, Section
from .user import User
from .subjects import Subject
from .period import Period

class TimetableEntry(Document):
    class_id = ReferenceField(Class, required=True)
    section_id = ReferenceField(Section, required=True)
    subject_id = ReferenceField(Subject, required=True)
    teacher_id = ReferenceField(User, required=True)
    period_id = ReferenceField(Period, required=True)
    room = StringField(required=False)
    day = StringField(required=True)  # Monday, Tuesday, ...

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "timetable"}

from mongoengine import Document, StringField, ReferenceField, BooleanField, DateTimeField
from datetime import datetime

from app.models.role import Role
from app.models.school import School


class User(Document):
    school_id = ReferenceField(School, required=True)
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField(required=True, unique=True)
    role = ReferenceField(Role, required=True)
    subject = StringField(required=True)
    password = StringField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"collection": "school_users"}

