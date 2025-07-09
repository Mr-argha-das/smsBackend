from fastapi import APIRouter
from app.models.announcement import Announcement
from app.schema.announcement import AnnouncementCreate, AnnouncementOut

announcement_router = APIRouter()

@announcement_router.post("/announcements", response_model=AnnouncementOut)
def create_announcement(data: AnnouncementCreate):
    announcement = Announcement(**data.dict()).save()
    return AnnouncementOut(
        id=str(announcement.id),
        created_at=announcement.created_at,
        **data.dict()
    )

@announcement_router.get("/announcements", response_model=list[AnnouncementOut])
def list_announcements():
    return [
        AnnouncementOut(
            id=str(a.id),
            title=a.title,
            message=a.message,
            audience=a.audience,
            created_at=a.created_at,
        )
        for a in Announcement.objects.order_by("-created_at")
    ]
