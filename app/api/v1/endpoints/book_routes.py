
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, APIRouter, HTTPException

from app.models.library_models import Book, IssueRecord, Reservation
from app.models.student import Student
from app.schema.library_schemas import BookIn, IssueIn, ReserveIn, ReturnIn
booksRouter = APIRouter()

@booksRouter.post("/book")
def add_book(book: BookIn):
    b = Book(**book.dict())
    b.available_copies = book.total_copies
    b.save()
    return str(b.id)

@booksRouter.put("/book/{book_id}")
def update_book(book_id: str, book: BookIn):
    b = Book.objects(id=book_id).first()
    if not b:
        raise HTTPException(404)
    b.update(**book.dict())
    return "updated"

@booksRouter.delete("/book/{book_id}")
def delete_book(book_id: str):
    b = Book.objects(id=book_id).first()
    if not b:
        raise HTTPException(404)
    b.is_deleted = True
    b.save()
    return "soft-deleted"

@booksRouter.get("/books")
def list_books(school_id: str, title: Optional[str] = None):
    query = Book.objects(school_id=school_id, is_deleted=False)
    if title:
        query = query.filter(title__icontains=title)
    return [{"id": str(b.id), "title": b.title, "author": b.author, "available": b.available_copies} for b in query]

@booksRouter.get("/book/{book_id}")
def get_book(book_id: str):
    b = Book.objects(id=book_id).first()
    if not b:
        raise HTTPException(404)
    return b

# TRANSACTIONS
@booksRouter.post("/issue")
def issue_book(data: IssueIn):
    book = Book.objects(id=data.book_id, school_id=data.school_id).first()
    student = Student.objects(id=data.student_id, school_id=data.school_id).first()
    if not book or not student:
        raise HTTPException(404)
    if book.available_copies < 1:
        raise HTTPException(400, "No copies available")
    book.available_copies -= 1
    book.save()
    issue = IssueRecord(
        school_id=data.school_id,
        student=student,
        book=book,
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    issue.save()
    return str(issue.id)

@booksRouter.post("/return")
def return_book(data: ReturnIn):
    issue = IssueRecord.objects(id=data.issue_id).first()
    if not issue:
        raise HTTPException(404)
    issue.return_date = datetime.utcnow()
    issue.is_returned = True
    issue.book.available_copies += 1
    issue.book.save()
    issue.save()
    return "returned"

@booksRouter.put("/renew/{issue_id}")
def renew_book(issue_id: str):
    issue = IssueRecord.objects(id=issue_id).first()
    if not issue or issue.is_returned:
        raise HTTPException(400)
    issue.due_date += timedelta(days=7)
    issue.save()
    return "renewed"

@booksRouter.post("/reserve")
def reserve_book(data: ReserveIn):
    reservation = Reservation(**data.dict())
    reservation.save()
    return str(reservation.id)

@booksRouter.delete("/reserve/{res_id}")
def cancel_reservation(res_id: str):
    r = Reservation.objects(id=res_id).first()
    if not r:
        raise HTTPException(404)
    r.delete()
    return "reservation cancelled"

# FINE & DUES
@booksRouter.get("/fine/{issue_id}")
def calculate_fine(issue_id: str):
    issue = IssueRecord.objects(id=issue_id).first()
    if not issue or issue.is_returned:
        return 0
    overdue_days = (datetime.utcnow() - issue.due_date).days
    return max(0, overdue_days * 5)  # ₹5 per day

@booksRouter.post("/pay-fine")
def pay_fine(issue_id: str):
    issue = IssueRecord.objects(id=issue_id).first()
    if not issue:
        raise HTTPException(404)
    issue.fine_paid = True
    issue.save()
    return "fine paid"

@booksRouter.get("/overdues")
def overdue_books(school_id: str):
    overdues = IssueRecord.objects(school_id=school_id, is_returned=False, due_date__lt=datetime.utcnow())
    return [{"student": str(r.student.id), "book": r.book.title, "due": r.due_date.isoformat()} for r in overdues]

# REPORTS
@booksRouter.get("/reports/inventory")
def inventory_report(school_id: str):
    books = Book.objects(school_id=school_id, is_deleted=False)
    return [{"title": b.title, "available": b.available_copies, "total": b.total_copies} for b in books]

@booksRouter.get("/reports/issued")
def issued_report(school_id: str):
    issues = IssueRecord.objects(school_id=school_id)
    return [{"book": i.book.title, "student": str(i.student.id), "issued_on": i.issue_date.isoformat()} for i in issues]

@booksRouter.get("/reports/overdue")
def overdue_report(school_id: str):
    return overdue_books(school_id)

@booksRouter.get("/reports/popular")
def popular_books(school_id: str):
    from mongoengine.queryset.visitor import Q
    books = Book.objects(school_id=school_id)
    result = []
    for book in books:
        count = IssueRecord.objects(book=book).count()
        result.append({"title": book.title, "count": count})
    return sorted(result, key=lambda x: -x["count"])

@booksRouter.get("/reports/student/{student_id}")
def student_report(student_id: str):
    records = IssueRecord.objects(student=student_id)
    return [{"book": r.book.title, "issue_date": r.issue_date.isoformat(), "returned": r.is_returned} for r in records]

# Register routes
