from enum import Enum
from effective_mobile_lib.application.schemas import BaseSchemaIn
from effective_mobile_lib.db.base import BaseDBM
from effective_mobile_interview.enumerations import BookStatus

# Входные данные для создания книги
class CreateBookIn(BaseSchemaIn):
    title: str
    author: str
    year: int
    book_status: str = BookStatus.AVAILABLE


# class SensitiveBookOut(BaseDBM):
#     title: str
#     author: str
#     year: int
#     book_status: str