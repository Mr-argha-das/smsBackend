from agent.model.script import StudentInfoModel
from fastapi import APIRouter, Depends, Form

from utils.auth import get_current_user
model = StudentInfoModel()
model.load_model("agent/pkl/student_info_model.pkl")

agent_router = APIRouter()

@agent_router.post("/ai-agent")
def ai_agent(urrent_user: dict = Depends(get_current_user), prompt: str = Form(...)):
    return {
        "message": "here is the data",
        "data": model.predict(prompt)
    }
