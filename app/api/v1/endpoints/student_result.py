from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from app.models.studentResult import StudentResult, SubjectMark, AcademicTerm
from app.models.subjects import Subject
from app.schema.result import ResultCreateSchema
from app.utils.result_utils import calculate_total, get_grade

result_router = APIRouter()

@result_router.post("/results")
async def create_result(data: ResultCreateSchema):
    """
    Create a new result record with term validation
    """
    # Validate term exists
    term = AcademicTerm.objects(id=data.term_id).first()
    if not term:
        raise HTTPException(status_code=400, detail=f"Term ID {data.term_id} not found")
    
    # Validate academic year matches term's academic year
    if data.academic_year != term.academic_year:
        raise HTTPException(
            status_code=400,
            detail=f"Academic year {data.academic_year} doesn't match term's academic year {term.academic_year}"
        )

    # Validate all subjects exist
    subject_marks = []
    for subject_data in data.subjects:
        subject = Subject.objects(id=subject_data.subject).first()
        if not subject:
            raise HTTPException(status_code=400, detail=f"Subject ID {subject_data.subject} not found")
        
        percentage = (subject_data.marks_obtained / subject_data.maximum_marks) * 100
        subject_marks.append(
            SubjectMark(
                subject=subject,
                marks_obtained=subject_data.marks_obtained,
                maximum_marks=subject_data.maximum_marks,
                grade=get_grade(percentage)
            )
        )

    # Calculate totals
    total_obtained, total_max, percentage = calculate_total(data.subjects)
    overall_grade = get_grade(percentage)

    # Create and save result
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
        percentage=percentage,
        overall_grade=overall_grade,
        rank_in_class=None,  # Will be calculated later
        result_status="Pass" if overall_grade != "F" else "Fail",
        exam_type=data.exam_type,
        exam_date=data.exam_date,
        result_published_date=data.result_published_date,
        term_id=term,  # Reference to AcademicTerm
        created_by=data.created_by,
        performance_trend=data.performance_trend,
        attendance_percentage=data.attendance_percentage,
        behavior_grade=data.behavior_grade,
        co_curricular_performance=data.co_curricular_performance
    )
    result.save()
    
    return {
        "message": "Result created successfully",
        "result_id": str(result.id),
        "term": term.name,
        "academic_year": term.academic_year
    }

@result_router.get("/results/{result_id}")
async def get_result(result_id: str):
    """
    Get a specific result by ID with term details
    """
    result = StudentResult.objects(id=result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    result_data = result.to_mongo().to_dict()
    term = AcademicTerm.objects(id=result.term_id.id).first()
    
    if term:
        result_data['term_details'] = {
            "name": term.name,
            "start_date": term.start_date,
            "end_date": term.end_date,
            "weightage": term.weightage
        }
    
    return result_data

@result_router.get("/results/student/{student_id}")
async def get_student_results(student_id: str):
    """
    Get all results for a specific student with term details
    """
    results = StudentResult.objects(student_id=student_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this student")
    
    response = []
    for result in results:
        result_data = result.to_mongo().to_dict()
        term = AcademicTerm.objects(id=result.term_id.id).first()
        
        if term:
            result_data['term_details'] = {
                "name": term.name,
                "academic_year": term.academic_year,
                "weightage": term.weightage
            }
        
        response.append(result_data)
    
    return response

@result_router.get("/results/class/{class_id}")
async def get_class_results(class_id: str):
    """
    Get all results for a specific class
    """
    results = StudentResult.objects(class_id=class_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this class")
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/section/{section_id}")
async def get_section_results(section_id: str):
    """
    Get all results for a specific section
    """
    results = StudentResult.objects(section_id=section_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this section")
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/school/{school_id}")
async def get_school_results(school_id: str):
    """
    Get all results for a specific school
    """
    results = StudentResult.objects(school_id=school_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this school")
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/term/{term_id}")
async def get_term_results(term_id: str):
    """
    Get all results for a specific academic term
    """
    term = AcademicTerm.objects(id=term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    results = StudentResult.objects(term_id=term_id)
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this term")
    
    response = []
    for result in results:
        result_data = result.to_mongo().to_dict()
        result_data['term_name'] = term.name
        response.append(result_data)
    
    return response

@result_router.get("/results/filter")
async def filter_results(
    school_id: Optional[str] = Query(None),
    class_id: Optional[str] = Query(None),
    section_id: Optional[str] = Query(None),
    term_id: Optional[str] = Query(None),
    academic_year: Optional[str] = Query(None),
    exam_type: Optional[str] = Query(None),
    min_percentage: Optional[float] = Query(None),
    max_percentage: Optional[float] = Query(None)
):
    """
    Filter results with multiple parameters
    """
    query = {}
    if school_id:
        query["school_id"] = school_id
    if class_id:
        query["class_id"] = class_id
    if section_id:
        query["section_id"] = section_id
    if term_id:
        query["term_id"] = term_id
    if academic_year:
        query["academic_year"] = academic_year
    if exam_type:
        query["exam_type"] = exam_type
    if min_percentage is not None:
        query["percentage__gte"] = min_percentage
    if max_percentage is not None:
        query["percentage__lte"] = max_percentage

    results = StudentResult.objects(__raw__=query)
    if not results:
        raise HTTPException(status_code=404, detail="No results found with given filters")
    
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/results/star-students/{school_id}")
async def get_star_students(
    school_id: str,
    min_percentage: float = 90.0,
    term_id: Optional[str] = Query(None)
):
    """
    Get top performing students (star students) for a school
    """
    query = {
        "school_id": school_id,
        "percentage__gte": min_percentage
    }
    
    if term_id:
        query["term_id"] = term_id
    
    results = StudentResult.objects(__raw__=query).order_by("-percentage")
    if not results:
        raise HTTPException(status_code=404, detail="No star students found")
    
    return [r.to_mongo().to_dict() for r in results]

@result_router.get("/terms/{school_id}")
async def get_school_terms(school_id: str):
    """
    Get all academic terms for a school
    """
    terms = AcademicTerm.objects(school_id=school_id).order_by("-start_date")
    return [t.to_mongo().to_dict() for t in terms]