from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from config import OPENAI_API_KEY
from students.model.student import Student
from adminSchools.model.table import School
from classes.model.table import Class, Section
from users.models.table import User
from students.model.fees_status import FeePaymentStatus
import openai
import json

client = openai.OpenAI(api_key=OPENAI_API_KEY)
ai_router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


def document_list_to_text(docs, table_name):
    lines = [f"Table: {table_name}"]
    for doc in docs:
        try:
            field_lines = []
            for field in doc._fields:
                value = getattr(doc, field, None)
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                elif hasattr(value, 'to_mongo'):
                    value = str(value.id)
                field_lines.append(f"{field} is {value}")
            lines.append("; ".join(field_lines))
        except Exception as e:
            lines.append(f"Error reading {table_name}: {e}")
    return "\n".join(lines)


def build_context():
    try:
        students = Student.objects()
        teachers = User.objects()
        classes = Class.objects()
        sections = Section.objects()
        schools = School.objects()

        context_parts = [
            document_list_to_text(schools, "Schools"),
            document_list_to_text(classes, "Classes"),
            document_list_to_text(sections, "Sections"),
            document_list_to_text(students, "Students"),
            document_list_to_text(teachers, "Teachers")
        ]
        return "\n".join(context_parts)

    except Exception as e:
        return f"Error building context: {e}"


def ask_gpt_question(context, question):
    try:
        system_prompt = (
            "You are an intelligent assistant for school management system.\n"
            "Always return response in the following JSON format:\n\n"
            "{\n"
            "  \"type\": \"text\" | \"table\" | \"error\",\n"
            "  \"data\": string OR list,\n"
            "  \"html\": string or null\n"
            "}\n\n"
            "If the answer is a list (like students or fees), then type should be 'table', "
            "data should be a list of objects, and html must contain a table with proper headers and rows.\n"
            "If it's just a text reply, set type='text'.\n"
            "Always return valid JSON only."
        )

        response = client.chat.completions.create(
            model="gpt-4o-min",  # or gpt-4-turbo / gpt-4o if allowed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}"},
                {"role": "user", "content": f"Question: {question}"}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        try:
            json_data = json.loads(content)
            return json_data
        except json.JSONDecodeError:
            return {
                "type": "text",
                "data": content,
                "html": None
            }

    except Exception as e:
        return {
            "type": "error",
            "data": str(e),
            "html": None
        }


@ai_router.post("/ask")
def ask_question(payload: QuestionRequest):
    context = build_context()
    if context.startswith("Error"):
        return {
            "question": payload.question,
            "response": {
                "type": "error",
                "data": context,
                "html": None
            },
            "success": False
        }

    result = ask_gpt_question(context, payload.question)

    return {
        "question": payload.question,
        "response": result,
        "success": result.get("type") != "error"
    }
