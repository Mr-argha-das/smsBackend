# main.py

from fastapi import FastAPI, Request, APIRouter

from app.schema.agent_schema import execute_mongoengine_code
from app.services.gpt_engine import ask_chatgpt
from pydantic import BaseModel


class AIRequest(BaseModel):
    query: str
    school_id:str
    role: str

ai_agent_router = APIRouter()

# Load system prompt once
with open("prompts/zodex_ai_system_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

@ai_agent_router.post("/ask")
async def ask_agent(request: AIRequest):

    
    gpt_code = ask_chatgpt(SYSTEM_PROMPT, request.query,  request.role,request.school_id)
    print("GPT Generated Code:\n", gpt_code)

    result = execute_mongoengine_code(gpt_code)

    return {
        "query": request.query,
        "code_generated": gpt_code,
        "result": result
    }
