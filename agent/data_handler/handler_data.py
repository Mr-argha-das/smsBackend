import json
from bson import ObjectId, json_util
from mongoengine.queryset.visitor import Q
from mongoengine import connect

from students.model.student import Student
from classes.model.table import Section, Class



# 🔁 Function selector
def functionSelector(intent, id: str):
    if not id:
        raise ValueError("ID is required.")

    if intent['intent'] == 'get_student_info':
        return get_student_info(intent.get('name', ""), id)
    if intent['intent'] == 'get_Students_by_class':
        return get_Students_by_class(intent.get('class', ""), id)
    if intent['intent'] == 'get_all_pending_fess':
        return get_all_pending_fess(school_id=id)
    
    return {"error": "Unknown intent"}

# ✅ Get students by name + REQUIRED ID
def get_student_info(name: str, id: str):
    try:
        object_id = ObjectId(id)
    except:
        raise ValueError("Invalid ObjectId.")

    query = Q(school_id=object_id)

    if name:
        parts = name.strip().split()
        name_query = Q()
        for part in parts:
            name_query |= Q(first_name__icontains=part) | Q(last_name__icontains=part)
        query &= name_query  # ensure id + name match both

    students = Student.objects(query)
    raw_data = [json.loads(json_util.dumps(student.to_mongo())) for student in students]
    dataLen = len(raw_data)

    for student in raw_data:
        try:
            class_oid = student['class_id']['$oid']
            section_oid = student['section_id']['$oid']
            classes = Class.objects.get(id=ObjectId(class_oid))
            section = Section.objects.get(id=ObjectId(section_oid))
            student['class_id'] = json.loads(json_util.dumps(classes.to_mongo()))
            student['section_id'] = json.loads(json_util.dumps(section.to_mongo()))
        except Exception as e:
            student['class_id'] = {"error": f"Class fetch failed: {str(e)}"}
            student['section_id'] = {"error": f"Section fetch failed: {str(e)}"}

    return {
        "message": f"Students matching ID '{id}'",
        "@type": "get_student_info",
        "@hasMultiple": dataLen > 1,
        "@hasMultipleMessage": "" if dataLen == 1 else "Choose which student",
        "data": raw_data
    }

# ✅ Get Class by name + REQUIRED ID
def get_Students_by_class(class_name: str, id: str):
    try:
        object_id = ObjectId(id)
    except:
        raise ValueError("Invalid ObjectId.")

    query = Q(school_id=object_id)

    if class_name:
        query &= Q(class_name__icontains=class_name)  # Combine both filters

    classes = Class.objects(query).first()
    students = Student.objects(class_id=ObjectId(classes.id))
    print(ObjectId(classes.id))
    return {
        "message": f"Classes matching ID '{id}'",
        "@type": "get_Students_by_class",
        "data": json.loads(students.to_json())
    }


def get_all_pending_fess(school_id: str):
    students = Student.objects(school_id=school_id)
    pending_list = []
    for student in students:
        pending_terms = [fee.term_name for fee in student.fee_status if not fee.paid]
        if pending_terms:
            pending_list.append({
                "student_id": str(student.id),
                "name": f"{student.first_name} {student.last_name}",
                "pending_terms": pending_terms
            })
    return {
        "message": f"all peending fess student",
        "@type": "get_all_pending_fess",
        "data": pending_list
    }