def calculate_total(subjects: list) -> tuple:
    total_obtained = sum([s['marks_obtained'] for s in subjects])
    total_max = sum([s['maximum_marks'] for s in subjects])
    percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0
    return total_obtained, total_max, percentage


def get_grade(percentage: float) -> str:
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "F"
