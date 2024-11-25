from enum import Enum


class BookStatus:
    """Диапозон значений для статуса книги"""
    AVAILABLE = "В наличии"
    CHECKED_OUT = "Выдана"

    @staticmethod
    def set() -> set:
        return {"В наличии", "Выдана"}