from fastapi import APIRouter
from app.models.log import CommunicationLog
from app.schema.log import CommunicationLogCreate, CommunicationLogOut

log_router = APIRouter()

@log_router.post("/logs/", response_model=CommunicationLogOut)
def create_log(data: CommunicationLogCreate):
    log = CommunicationLog(**data.dict()).save()
    return CommunicationLogOut(
        id=str(log.id), sender_id=str(log.sender.id), receiver_id=str(log.receiver.id),
        message=log.message, type=log.type, timestamp=log.timestamp
    )

@log_router.get("/logs/", response_model=list[CommunicationLogOut])
def get_logs():
    return [
        CommunicationLogOut(
            id=str(log.id), sender_id=str(log.sender.id), receiver_id=str(log.receiver.id),
            message=log.message, type=log.type, timestamp=log.timestamp
        ) for log in CommunicationLog.objects.order_by("-timestamp")
    ]
