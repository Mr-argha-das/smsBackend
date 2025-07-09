from fastapi import APIRouter

from app.models.notification import Notification
from app.schema.notification import NotificationCreate, NotificationOut

notification_router = APIRouter()

@notification_router.post("/notification", response_model=NotificationOut)
def create_notification(data: NotificationCreate):
    notification = Notification(**data.dict()).save()
    return NotificationOut(
        id=str(notification.id), user_id=str(notification.user.id),
        content=notification.content, is_read=notification.is_read,
        created_at=notification.created_at
    )

@notification_router.get("/notification/user/{user_id}", response_model=list[NotificationOut])
def get_user_notifications(user_id: str):
    notifications = Notification.objects.filter(user=user_id).order_by("-created_at")
    return [
        NotificationOut(
            id=str(n.id), user_id=str(n.user.id), content=n.content,
            is_read=n.is_read, created_at=n.created_at
        ) for n in notifications
    ]
