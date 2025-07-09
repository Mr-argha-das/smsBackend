from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.studentResult import StudentResult, SubjectMark
from app.models.subjects import Subject
from app.schema.result import ResultCreateSchema
from app.utils.result_utils import calculate_total, get_grade

result_router = APIRouter()


@result_router.post("/results")
def create_result(data: ResultCreateSchema):
    # Validate subject references
    subject_marks = []
    for s in data.subjects:
        subject_obj = Subject.objects(id=s.subject).first()
        if not subject_obj:
            raise HTTPException(status_code=400, detail=f"Subject ID {s.subject} not found")
        
        subject_marks.append(
            SubjectMark(
                subject=subject_obj,
                marks_obtained=s.marks_obtained,
                maximum_marks=s.maximum_marks,
                grade=get_grade((s.marks_obtained / s.maximum_marks) * 100)
            )
        )

    total_obtained, total_max, percent = calculate_total(data.subjects)
    overall_grade = get_grade(percent)

    result = StudentResult(

        student_id=data.student_id,
        student_name=data.student_name,
        class_id=data.class_id,
        section_id=data.section_id,
        roll_number=data.roll_number,
        school_id=data.school_id,
        academic_year=data.academic_year,
        subjects=subject_marks,
        total_marks_obtained=total_obtained,
        total_maximum_marks=total_max,
        percentage=percent,
        overall_grade=overall_grade,
        rank_in_class=None,
        result_status="Pass" if overall_grade != "F" else "Fail",

        exam_type=data.exam_type,
        exam_date=data.exam_date,
        result_published_date=data.result_published_date,
        term_id=data.term_id,

        created_by=data.created_by,
        performance_trend=data.performance_trend,
        attendance_percentage=data.attendance_percentage,
        behavior_grade=data.behavior_grade,
        co_curricular_performance=data.co_curricular_performance
    )
    result.save()
    return {"message": "Result created", "id": str(result.id)}


@result_router.get("/results/{student_id}")
def get_result_by_student(student_id: str):
    result = StudentResult.objects(student_id=student_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result.to_mongo().to_dict()


@result_router.get("/results")
def list_results():
    results = StudentResult.objects()
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/by-class")
def get_results_by_class(class_id: str):
    results = StudentResult.objects(class_id=class_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this class")
    return [r.to_mongo().to_dict() for r in results]


@result_router.get("/results/by-section")
def get_results_by_section(section_id: str):
    results = StudentResult.objects(section_id=section_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this section")
    return [r.to_mongo().to_dict() for r in results]


@result_router.get("/results/by-school")
def get_results_by_school(school_id: str):
    results = StudentResult.objects(school_id=school_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this school")
    return [r.to_mongo().to_dict() for r in results]


@result_router.get("/results/search")
def filter_results(
    class_id: Optional[str] = Query(None),
    section_id: Optional[str] = Query(None),
    school_id: Optional[str] = Query(None),
    academic_year: Optional[str] = Query(None),
    exam_type: Optional[str] = Query(None)
):
    query = {}
    if class_id:
        query["class_id"] = class_id
    if section_id:
        query["section_id"] = section_id
    if school_id:
        query["school_id"] = school_id
    if academic_year:
        query["academic_year"] = academic_year
    if exam_type:
        query["exam_type"] = exam_type

    results = StudentResult.objects(__raw__=query)
    if not results:
        raise HTTPException(status_code=404, detail="No results found with given filters")
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/star-students")
def get_star_students_by_school(school_id: str, min_percentage: float = 90.0):
    results = StudentResult.objects(school_id=school_id, percentage__gte=min_percentage)
    if not results:
        raise HTTPException(status_code=404, detail="No star students found for this school")
    return [r.to_mongo().to_dict() for r in results]