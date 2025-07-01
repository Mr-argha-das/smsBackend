import json
from agent.data_handler.handler_data import functionSelector, get_student_info
from agent.model.script import StudentInfoModel
from fastapi import APIRouter, Depends, Form

from app.schema.auth import get_current_user
model = StudentInfoModel()
model.load_model("agent/pkl/student_info_model.pkl")

agent_router = APIRouter()


@agent_router.post("/ai-agent")
def ai_agent(current_user: dict = Depends(get_current_user), prompt: str = Form(...), school_id: str = Form(...)):
    intent = model.predict(prompt)  # This is already a dict

    return functionSelector(intent=intent, id=school_id)

