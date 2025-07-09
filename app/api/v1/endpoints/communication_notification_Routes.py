from fastapi import APIRouter

from app.models.announcement import Announcement
from app.models.feedback import Feedback
from app.models.log import CommunicationLog
from app.models.notification import Notification
from app.schema.announcement import AnnouncementCreate, AnnouncementOut
from app.schema.feedback import FeedbackCreate, FeedbackOut
from app.schema.log import CommunicationLogCreate, CommunicationLogOut
from app.schema.notification import NotificationCreate, NotificationOut


communication_router = APIRouter()

@communication_router.post("/feedback", response_model=FeedbackOut)
def create_feedback(data: FeedbackCreate):
    feedback = Feedback(**data.dict()).save()
    return FeedbackOut(
        id=str(feedback.id), user_id=str(feedback.user.id),
        subject=feedback.subject, message=feedback.message,
        status=feedback.status, created_at=feedback.created_at
    )

@communication_router.get("/feedback", response_model=list[FeedbackOut])
def list_feedback():
    return [
        FeedbackOut(
            id=str(f.id), user_id=str(f.user.id),
            subject=f.subject, message=f.message,
            status=f.status, created_at=f.created_at
        ) for f in Feedback.objects.order_by("-created_at")
    ]



# 
@communication_router.post("/logs/", response_model=CommunicationLogOut)
def create_log(data: CommunicationLogCreate):
    log = CommunicationLog(**data.dict()).save()
    return CommunicationLogOut(
        id=str(log.id), sender_id=str(log.sender.id), receiver_id=str(log.receiver.id),
        message=log.message, type=log.type, timestamp=log.timestamp
    )

@communication_router.get("/logs/", response_model=list[CommunicationLogOut])
def get_logs():
    return [
        CommunicationLogOut(
            id=str(log.id), sender_id=str(log.sender.id), receiver_id=str(log.receiver.id),
            message=log.message, type=log.type, timestamp=log.timestamp
        ) for log in CommunicationLog.objects.order_by("-timestamp")
    ]
# 


@communication_router.post("/notification", response_model=NotificationOut)
def create_notification(data: NotificationCreate):
    notification = Notification(**data.dict()).save()
    return NotificationOut(
        id=str(notification.id), user_id=str(notification.user.id),
        content=notification.content, is_read=notification.is_read,
        created_at=notification.created_at
    )

@communication_router.get("/notification/user/{user_id}", response_model=list[NotificationOut])
def get_user_notifications(user_id: str):
    notifications = Notification.objects.filter(user=user_id).order_by("-created_at")
    return [
        NotificationOut(
            id=str(n.id), user_id=str(n.user.id), content=n.content,
            is_read=n.is_read, created_at=n.created_at
        ) for n in notifications
    ]


@communication_router.post("/announcements", response_model=AnnouncementOut)
def create_announcement(data: AnnouncementCreate):
    announcement = Announcement(**data.dict()).save()
    return AnnouncementOut(
        id=str(announcement.id),
        created_at=announcement.created_at,
        **data.dict()
    )

@communication_router.get("/announcements", response_model=list[AnnouncementOut])
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
