
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional, List
from app.models.studentResult import AcademicTerm, StudentResult
from app.models.school import School
from app.schema.terms_schema import TermCreateSchema, TermUpdateSchema

term_router = APIRouter()

@term_router.post("/", response_description="Create new academic term")
async def create_term(term: TermCreateSchema):
    # Validate school exists
    school = School.objects(id=term.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Check if term with same name/year already exists
    existing_term = AcademicTerm.objects(
        school_id=term.school_id,
        academic_year=term.academic_year,
        name=term.name
    ).first()
    
    if existing_term:
        raise HTTPException(
            status_code=400,
            detail="Term with this name already exists for the given academic year"
        )
    
    # Validate dates
    if term.start_date >= term.end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )
    
    new_term = AcademicTerm(
        school_id=school,
        name=term.name,
        academic_year=term.academic_year,
        start_date=term.start_date,
        end_date=term.end_date,
        weightage=term.weightage,
        is_active=term.is_active
    )
    new_term.save()
    
    return {
        "message": "Academic term created successfully",
        "term_id": str(new_term.id),
        "term_name": new_term.name
    }

@term_router.get("/{term_id}", response_description="Get single term details")
async def get_term(term_id: str):
    term = AcademicTerm.objects(id=term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    return term.to_mongo().to_dict()

@term_router.get("/school/{school_id}", response_description="Get all terms for a school")
async def get_school_terms(
    school_id: str,
    active_only: Optional[bool] = Query(True),
    academic_year: Optional[str] = Query(None)
):
    query = {"school_id": school_id}
    
    if active_only:
        query["is_active"] = True
    
    if academic_year:
        query["academic_year"] = academic_year
    
    terms = AcademicTerm.objects(__raw__=query).order_by("-start_date")
    return [t.to_mongo().to_dict() for t in terms]

@term_router.put("/{term_id}", response_description="Update term details")
async def update_term(term_id: str, term_data: TermUpdateSchema):
    term = AcademicTerm.objects(id=term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    update_data = term_data.dict(exclude_unset=True)
    
    # Validate dates if being updated
    if 'start_date' in update_data or 'end_date' in update_data:
        start_date = update_data.get('start_date', term.start_date)
        end_date = update_data.get('end_date', term.end_date)
        if start_date >= end_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )
    
    # Update fields
    for field, value in update_data.items():
        setattr(term, field, value)
    
    term.save()
    return {
        "message": "Term updated successfully",
        "term_id": str(term.id)
    }

@term_router.delete("/{term_id}", response_description="Delete academic term")
async def delete_term(term_id: str):
    term = AcademicTerm.objects(id=term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    # Check if any results are associated with this term
    results_count = StudentResult.objects(term_id=term_id).count()
    if results_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete term - {results_count} results are associated with it"
        )
    
    term.delete()
    return {"message": "Term deleted successfully"}

@term_router.get("/current/{school_id}", response_description="Get current active term")
async def get_current_term(school_id: str):
    today = datetime.utcnow()
    
    current_term = AcademicTerm.objects(
        school_id=school_id,
        start_date__lte=today,
        end_date__gte=today,
        is_active=True
    ).order_by("-start_date").first()
    
    if not current_term:
        raise HTTPException(
            status_code=404,
            detail="No active term found for current date"
        )
    
    return current_term.to_mongo().to_dict()

@term_router.get("/upcoming/{school_id}", response_description="Get upcoming terms")
async def get_upcoming_terms(school_id: str, limit: int = Query(3, ge=1)):
    today = datetime.utcnow()
    
    upcoming_terms = AcademicTerm.objects(
        school_id=school_id,
        start_date__gt=today,
        is_active=True
    ).order_by("start_date").limit(limit)
    
    return [t.to_mongo().to_dict() for t in upcoming_terms]
