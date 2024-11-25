from effective_mobile_interview.enumerations import BookStatus
from effective_mobile_lib.db.base import BaseDBM, BaseFields


class BookFields(BaseFields):
    """Поля для книга"""
    title = "title"
    author = "author"
    year = "year"
    book_status = "book_status"

class BookDBM(BaseDBM):
    """Модель книги в БД"""
    title: str
    author: str
    year: int
    book_status: str

    def __repr__(self) -> str:
        return f"Название книги: {self.title}\nАвтор: {self.author}\nГод издания: {self.year}\nСтатус: {self.book_status}\nid: {self.id}\n"