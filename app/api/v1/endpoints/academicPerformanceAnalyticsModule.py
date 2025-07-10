from fastapi import APIRouter

from app.services.academicPerformanceAnalyticsModule_service import get_class_wise_performance, get_pass_fail_count, get_subject_wise_distribution, get_top_performers

academicPerformanceAnalyticsModule = APIRouter()

@academicPerformanceAnalyticsModule.get("/report/results/subject-distribution")
def subject_distribution(school_id: str, exam_type: str = None):
    data = get_subject_wise_distribution(school_id, exam_type)

    labels = []
    avg_data = []
    max_data = []
    min_data = []

    for item in data:
        subject_id = str(item["_id"])
        labels.append(subject_id)
        avg_data.append(round(item["average"], 2))
        max_data.append(item["max"])
        min_data.append(item["min"])

    return {
        "labels": labels,
        "datasets": [
            {"label": "Average Marks", "data": avg_data},
            {"label": "Max Marks", "data": max_data},
            {"label": "Min Marks", "data": min_data}
        ]
    }

@academicPerformanceAnalyticsModule.get("/report/results/class-average")
def class_average(school_id: str, exam_type: str = None):
    data = get_class_wise_performance(school_id, exam_type)
    labels = []
    values = []

    for item in data:
        labels.append(str(item["_id"]))
        values.append(round(item["average_percentage"], 2))

    return {
        "labels": labels,
        "datasets": [
            {"label": "Average %", "data": values}
        ]
    }

@academicPerformanceAnalyticsModule.get("/report/results/top-performers")
def top_performers(school_id: str, class_id: str = None, exam_type: str = None):
    students = get_top_performers(school_id, class_id, exam_type)

    return {
        "top_students": [
            {
                "name": s.student_name,
                "percentage": s.percentage,
                "class_id": str(s.class_id.id),
                "rank": s.rank_in_class
            } for s in students
        ]
    }

@academicPerformanceAnalyticsModule.get("/report/results/pass-fail")
def pass_fail_summary(school_id: str, exam_type: str = None):
    data = get_pass_fail_count(school_id, exam_type)

    labels = []
    values = []
    for item in data:
        labels.append(item["_id"])
        values.append(item["count"])

    return {
        "labels": labels,
        "data": values
    }

