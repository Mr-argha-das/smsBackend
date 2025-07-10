from fastapi import APIRouter, HTTPException, Query
from app.models.exam_seating import Room
from app.schema.exam_seating import RoomCreateSchema, RoomUpdateSchema
from datetime import datetime
from typing import Optional

room_router = APIRouter()

@room_router.post("/rooms")
def create_room(data: RoomCreateSchema):
    existing = Room.objects(school_id=data.school_id, name=data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room with this name already exists in the school")

    room = Room(**data.dict())
    room.save()
    return {"message": "Room created", "room_id": str(room.id)}


@room_router.get("/rooms")
def list_rooms(school_id: str, room_type: Optional[str] = Query(None)):
    query = {"school_id": school_id}
    if room_type:
        query["room_type"] = room_type
    rooms = Room.objects(__raw__=query)
    return [r.to_mongo().to_dict() for r in rooms]


@room_router.get("/rooms/{room_id}")
def get_room(room_id: str):
    room = Room.objects(id=room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room.to_mongo().to_dict()


@room_router.put("/rooms/{room_id}")
def update_room(room_id: str, data: RoomUpdateSchema):
    room = Room.objects(id=room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(room, field, value)

    room.updated_at = datetime.utcnow()
    room.save()
    return {"message": "Room updated"}


@room_router.delete("/rooms/{room_id}")
def delete_room(room_id: str):
    room = Room.objects(id=room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.delete()
    return {"message": "Room deleted successfully"}
