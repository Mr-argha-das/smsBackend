from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.subjects import Subject
from app.schema.auth import get_current_user
from app.schema.subject_schema import SubjectCreate, SubjectUpdate, SubjectResponse
from bson import ObjectId

subject_router = APIRouter()

@subject_router.post("/", response_model=SubjectResponse)
def create_subject(data: SubjectCreate,  current_user: dict = Depends(get_current_user),):
    subject = Subject(**data.dict())
    subject.save()
    return SubjectResponse(id=str(subject.id), **data.dict(), created_at=subject.created_at, updated_at=subject.updated_at)

@subject_router.get("/{class_id}", response_model=List[SubjectResponse])
def get_all_subjects(  class_id: str, current_user: dict = Depends(get_current_user),):
    subjects = Subject.objects(class_id=class_id).all()
    return [SubjectResponse(
        id=str(sub.id),
        school_id=str(sub.school_id.id),
        class_id=str(sub.class_id.id),
        section_id=str(sub.section_id.id) if sub.section_id else None,
        subject_name=sub.subject_name,
        subject_code=sub.subject_code,
        assigned_teachers=[str(t.id) for t in sub.assigned_teachers],
        syllabus=sub.syllabus,
        created_at=sub.created_at,
        updated_at=sub.updated_at
    ) for sub in subjects]

@subject_router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: str,  current_user: dict = Depends(get_current_user),):
    subject = Subject.objects(id=subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return SubjectResponse(
        id=str(subject.id),
        school_id=str(subject.school_id.id),
        class_id=str(subject.class_id.id),
        section_id=str(subject.section_id.id) if subject.section_id else None,
        subject_name=subject.subject_name,
        subject_code=subject.subject_code,
        assigned_teachers=[str(t.id) for t in subject.assigned_teachers],
        syllabus=subject.syllabus,
        created_at=subject.created_at,
        updated_at=subject.updated_at
    )

@subject_router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: str, data: SubjectUpdate,  current_user: dict = Depends(get_current_user),):
    subject = Subject.objects(id=subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(subject, key, value)
    subject.save()
    return get_subject(subject_id)

@subject_router.delete("/{subject_id}")
def delete_subject(subject_id: str,  current_user: dict = Depends(get_current_user),):
    subject = Subject.objects(id=subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    subject.delete()
    return {"message": "Subject deleted successfully"}
