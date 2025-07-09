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
