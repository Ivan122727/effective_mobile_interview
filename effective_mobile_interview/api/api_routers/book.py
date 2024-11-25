from copy import deepcopy
from effective_mobile_lib.application.router import Router
from effective_mobile_lib.application.schemas import BaseSchemaOut
from effective_mobile_interview.api.schemas.book import CreateBookIn
from effective_mobile_interview.db.library_db import db
from effective_mobile_interview.db.collections.book import BookFields
from effective_mobile_interview.enumerations import BookStatus

api_router = Router()

# Добавление книги
@api_router.post("/book.add")
def add_book(
    book: CreateBookIn
):
    book_id: int = db.insert_document(book.to_doc())
    return BaseSchemaOut(status=200, result={"is_done": True})

# Удаление книги
@api_router.delete("/book.delete")
def delete_book(
    book_id: int    
):
    book = db.find_by_index(BookFields.id, book_id)
    is_done = False
    if book:
        db.delete_document(BookFields.id, book_id)
        is_done = True
    return BaseSchemaOut(status=200, result={"is_done": is_done})

# Поиск книги: title
@api_router.get("/book.search_by_title")
def search_book_by_title(expression: str):
    return BaseSchemaOut(status=200, result={"books": db.search_docs(expression, BookFields.title)})

# Поиск книги: author
@api_router.get("/book.search_by_author")
def search_book_by_author(expression: str):
    return BaseSchemaOut(status=200, result={"books": db.search_docs(expression, BookFields.author)})

# Поиск книги: year
@api_router.get("/book.search_by_year")
def search_book_by_year(expression: str):
    return BaseSchemaOut(status=200, result={"books": db.search_docs(expression, BookFields.year)})

# Отображение всех книг
@api_router.get("/book.get_all_books")
def get_all_books():
    founded_books = db.get_all_items()
    return BaseSchemaOut(status=200, result={"books": founded_books})

# Изменение статуса книги
@api_router.patch("/book.change_status")
def change_status(
    id: int,
    book_status: str
):
    is_done = False
    book = db.find_by_index(BookFields.id, id)
    if book and book_status in BookStatus.set():
        db.update_by_index(BookFields.id, id, {BookFields.book_status: book_status})
        is_done = True
    elif book and book_status not in BookStatus.set():
        return BaseSchemaOut(status=424, result=f"Invalid parameter {book_status}")
    return BaseSchemaOut(status=404, result={"is_done": is_done})
