from app.models.studentResult import StudentResult
from bson import ObjectId

def get_subject_wise_distribution(school_id, exam_type=None):
    match = {"school_id": ObjectId(school_id)}
    if exam_type:
        match["exam_type"] = exam_type

    pipeline = [
        {"$match": match},
        {"$unwind": "$subjects"},
        {
            "$group": {
                "_id": "$subjects.subject",
                "average": {"$avg": "$subjects.marks_obtained"},
                "max": {"$max": "$subjects.marks_obtained"},
                "min": {"$min": "$subjects.marks_obtained"}
            }
        }
    ]
    return list(StudentResult.objects.aggregate(*pipeline))

def get_class_wise_performance(school_id, exam_type=None):
    match = {"school_id": ObjectId(school_id)}
    if exam_type:
        match["exam_type"] = exam_type

    pipeline = [
        {"$match": match},
        {
            "$group": {
                "_id": "$class_id",
                "average_percentage": {"$avg": "$percentage"}
            }
        }
    ]
    return list(StudentResult.objects.aggregate(*pipeline))

def get_top_performers(school_id, class_id=None, exam_type=None, limit=5):
    query = {"school_id": ObjectId(school_id)}
    if class_id:
        query["class_id"] = ObjectId(class_id)
    if exam_type:
        query["exam_type"] = exam_type

    top_students = StudentResult.objects(**query).order_by("-percentage").limit(limit)
    return top_students

def get_pass_fail_count(school_id, exam_type=None):
    match = {"school_id": ObjectId(school_id)}
    if exam_type:
        match["exam_type"] = exam_type

    pipeline = [
        {"$match": match},
        {
            "$group": {
                "_id": "$result_status",
                "count": {"$sum": 1}
            }
        }
    ]
    return list(StudentResult.objects.aggregate(*pipeline))
