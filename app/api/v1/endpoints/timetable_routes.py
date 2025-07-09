from fastapi import APIRouter, HTTPException
from typing import List
from app.models.timetable_entry import TimetableEntry
from app.models.period import Period
from app.schema.timetable_schema import TimetableCreate, TimetableOut,TimetableUpdate

import random
from app.models.timetable_entry import TimetableEntry
from app.models.user import User
from app.models.subjects import Subject
from app.models.period import Period
from app.models.classes import Class, Section
timeTableRoutes = APIRouter()

@timeTableRoutes.post("/", response_model=TimetableOut)
def create_timetable_entry(data: TimetableCreate):
    # 🔍 Check if this period is already used in same class/section
    if TimetableEntry.objects(
        class_id=data.class_id,
        section_id=data.section_id,
        day=data.day,
        period_id=data.period_id
    ):
        raise HTTPException(status_code=400, detail="This class already has a subject assigned for this period.")

    # 🔍 Check teacher conflict
    if TimetableEntry.objects(
        teacher_id=data.teacher_id,
        day=data.day,
        period_id=data.period_id
    ):
        raise HTTPException(status_code=400, detail="This teacher is already assigned in another class at this time.")

    # 🔍 Check room conflict (if room is given)
    if data.room:
        if TimetableEntry.objects(
            room=data.room,
            day=data.day,
            period_id=data.period_id
        ):
            raise HTTPException(status_code=400, detail="This room is already occupied at this time.")

    entry = TimetableEntry(**data.dict())
    entry.save()
    return TimetableOut(id=str(entry.id), **data.dict())

@timeTableRoutes.get("/class/{class_id}/{section_id}", response_model=List[TimetableOut])
def get_class_timetable(class_id: str, section_id: str):
    entries = TimetableEntry.objects(class_id=class_id, section_id=section_id).order_by('day', 'period_id')
    return [
        TimetableOut(
            id=str(e.id),
            class_id=str(e.class_id.id),
            section_id=str(e.section_id.id),
            subject_id=str(e.subject_id.id),
            teacher_id=str(e.teacher_id.id),
            period_id=str(e.period_id.id),
            room=e.room,
            day=e.day
        ) for e in entries
    ]

@timeTableRoutes.get("/teacher/{teacher_id}", response_model=List[TimetableOut])
def get_teacher_timetable(teacher_id: str):
    entries = TimetableEntry.objects(teacher_id=teacher_id).order_by('day', 'period_id')
    return [
        TimetableOut(
            id=str(e.id),
            class_id=str(e.class_id.id),
            section_id=str(e.section_id.id),
            subject_id=str(e.subject_id.id),
            teacher_id=str(e.teacher_id.id),
            period_id=str(e.period_id.id),
            room=e.room,
            day=e.day
        ) for e in entries
    ]


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def generate_auto_timetable(class_id, section_id):
    periods = Period.objects().order_by("order")
    subjects = Subject.objects(class_id=class_id)
    
    if not subjects:
        raise Exception("No subjects assigned to class.")

    teacher_ids = list(set([s.assigned_teachers[0].id for s in subjects if s.assigned_teachers]))

    timetable = []

    for day in DAYS:
        for period in periods:
            subject = random.choice(subjects)
            teacher = subject.assigned_teachers[0] if subject.assigned_teachers else None

            # Check if already assigned
            if TimetableEntry.objects(
                class_id=class_id, section_id=section_id,
                period_id=period.id, day=day
            ):
                continue

            # Conflict checking
            if TimetableEntry.objects(day=day, period_id=period.id, teacher_id=teacher.id):
                continue

            entry = TimetableEntry(
                class_id=class_id,
                section_id=section_id,
                subject_id=subject.id,
                teacher_id=teacher.id,
                period_id=period.id,
                day=day,
                room="Room 101"
            )
            entry.save()
            timetable.append(entry)

    return timetable


@timeTableRoutes.post("/generate/{class_id}/{section_id}")
def auto_generate_timetable(class_id: str, section_id: str):
    try:
        class_exists = Class.objects(id=class_id).first()
        section_exists = Section.objects(id=section_id).first()

        if not class_exists or not section_exists:
            raise HTTPException(status_code=404, detail="Class or section not found.")

        timetable = generate_auto_timetable(class_id, section_id)

        return {
            "message": f"Timetable generated successfully with {len(timetable)} entries.",
            "entries_created": len(timetable)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@timeTableRoutes.put("/{timetable_id}")
def update_timetable_entry(timetable_id: str, data: TimetableUpdate):
    entry = TimetableEntry.objects(id=timetable_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Timetable entry not found.")

    updates = data.dict(exclude_unset=True)

    # 👇 Conflict checks
    new_teacher = updates.get("teacher_id", str(entry.teacher_id.id))
    new_period = updates.get("period_id", str(entry.period_id.id))
    new_day = updates.get("day", entry.day)
    new_room = updates.get("room", entry.room)

    # Check teacher conflict
    if TimetableEntry.objects(
        teacher_id=new_teacher,
        period_id=new_period,
        day=new_day,
        id__ne=timetable_id
    ):
        raise HTTPException(status_code=400, detail="This teacher is already assigned in that time.")

    # Check room conflict
    if new_room:
        if TimetableEntry.objects(
            room=new_room,
            period_id=new_period,
            day=new_day,
            id__ne=timetable_id
        ):
            raise HTTPException(status_code=400, detail="Room is already occupied at that time.")

    # 👇 Apply updates
    for field, value in updates.items():
        setattr(entry, field, value)
    entry.save()

    return TimetableOut(
        id=str(entry.id),
        class_id=str(entry.class_id.id),
        section_id=str(entry.section_id.id),
        subject_id=str(entry.subject_id.id),
        teacher_id=str(entry.teacher_id.id),
        period_id=str(entry.period_id.id),
        room=entry.room,
        day=entry.day
    )