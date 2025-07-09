from fastapi import APIRouter
from app.models.feedback import Feedback
from app.schema.feedback import FeedbackCreate, FeedbackOut

feedback_router = APIRouter()

@feedback_router.post("/feedback", response_model=FeedbackOut)
def create_feedback(data: FeedbackCreate):
    feedback = Feedback(**data.dict()).save()
    return FeedbackOut(
        id=str(feedback.id), user_id=str(feedback.user.id),
        subject=feedback.subject, message=feedback.message,
        status=feedback.status, created_at=feedback.created_at
    )

@feedback_router.get("/feedback", response_model=list[FeedbackOut])
def list_feedback():
    return [
        FeedbackOut(
            id=str(f.id), user_id=str(f.user.id),
            subject=f.subject, message=f.message,
            status=f.status, created_at=f.created_at
        ) for f in Feedback.objects.order_by("-created_at")
    ]
