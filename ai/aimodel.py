from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from mongoengine import connect
from students.model.student import Student
from classes.model.table import Class
from users.models.table import User
from adminSchools.model.table import School
import re

# MongoDB connection
connect('smsTest', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/smsTest")

# Initialize FastAPI Router
ai_router = APIRouter()

# Pydantic model for request
class PromptRequest(BaseModel):
    prompt: str

# --- Prompt Interpretation Functions ---
def fetch_students_by_class(prompt):
    match = re.search(r'class\s*(\d+)', prompt)
    if match and "student" in prompt:
        class_name = match.group(1)
        cls = Class.objects(class_name=class_name).first()
        if cls:
            return {
                "model": Student,
                "filters": {"class_id": cls},
                "fields": ["first_name", "last_name", "roll_number"]
            }


def fetch_teacher_by_subject(prompt):
    subjects = ["maths", "science", "english", "hindi", "history"]
    for subject in subjects:
        if subject in prompt and "teacher" in prompt:
            return {
                "model": User,
                "filters": {"subject__iexact": subject},
                "fields": ["name", "email"]
            }

def fetch_school_by_city(prompt):
    match = re.search(r'(?:in|ke)\s+([a-zA-Z]+)', prompt)
    if "school" in prompt and match:
        city = match.group(1).capitalize()
        return {
            "model": School,
            "filters": {"city__iexact": city},
            "fields": ["school_name", "principal_name"]
        }

def fetch_student_profile_by_name(prompt):
    match = re.search(r'profile.*?([a-zA-Z]+)', prompt)
    if match:
        name = match.group(1)
        return {
            "model": Student,
            "filters": {"first_name__iexact": name},
            "fields": ["first_name", "last_name", "roll_number", "class_id", "dob", "address"]
        }

def update_student_name(prompt):
    match = re.search(r'roll\s*(\d+).*?naam\s*(\w+)', prompt)
    if match:
        roll = match.group(1)
        new_name = match.group(2)
        student = Student.objects(roll_number=roll).first()
        if student:
            student.first_name = new_name
            student.save()
            return {"message": f"Student name updated to {new_name} for roll {roll}"}
        return {"message": "Student not found"}

def add_new_student(prompt):
    match = re.search(r'add.*?student.*?(\w+)\s*,?\s*class\s*(\d+)', prompt)
    if match:
        name = match.group(1)
        class_name = match.group(2)
        student = Student(first_name=name, class_id=Class.objects(class_name=class_name).first())
        student.save()
        return {"message": f"Student {name} added to class {class_name}"}

def delete_student(prompt):
    match = re.search(r'delete.*?student.*?roll\s*(\d+)', prompt)
    if match:
        roll = match.group(1)
        student = Student.objects(roll_number=roll).first()
        if student:
            student.delete()
            return {"message": f"Student with roll {roll} deleted"}
        return {"message": "Student not found"}

# --- Central Prompt Interpreter ---
def interpret_prompt(prompt: str):
    prompt = prompt.lower()

    for updater in [update_student_name, add_new_student, delete_student]:
        result = updater(prompt)
        if result:
            return {"action": "update", "data": result}

    for fetcher in [
        fetch_students_by_class,
        fetch_teacher_by_subject,
        fetch_school_by_city,
        fetch_student_profile_by_name
    ]:
        result = fetcher(prompt)
        if result:
            return {"action": "query", "data": result}

    return None

# --- Query Executor ---
def execute_query(model, filters, fields):
    query = model.objects(**filters)
    results = []
    for doc in query:
        item = {}
        for field in fields:
            value = getattr(doc, field, None)
            item[field] = str(value) if value is not None else None
        results.append(item)
    return results

# --- FastAPI Endpoint ---
@ai_router.post("/query")
def handle_prompt_api(request: PromptRequest):
    parsed = interpret_prompt(request.prompt)
    if not parsed:
        raise HTTPException(status_code=400, detail="Prompt samajh nahi aaya ya match nahi hua.")

    if parsed.get("action") == "update":
        return parsed["data"]

    data = execute_query(parsed["data"]["model"], parsed["data"]["filters"], parsed["data"]["fields"])

    if len(data) > 1 and "profile" in request.prompt.lower():
        return {
            "message": f"{len(data)} students found with that name. Please specify roll number or class.",
            "options": data
        }

    return {"results": data}  

# Mounting this router to main FastAPI app should be done in your main.py like:
# from your_ai_file import ai_router
# app.include_router(ai_router, prefix="/ai")
