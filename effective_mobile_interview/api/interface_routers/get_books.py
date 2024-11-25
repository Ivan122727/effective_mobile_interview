from typing import Any
from xml.dom.minidom import Document
from effective_mobile_interview.db.collections.book import BookDBM
from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut


router = CommandInterFaceRouter()

def print_get_books_page():
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Вернуться на главную страницу")
    router.print_centered("2. Отобразить все книги")
    print("Действие номер: ", end="")

@router.post("/book/all")
def print_all_books(
    books: list[Document]
):
    router.print_centered(f"Найдено книг: {len(books)}")
    for book in books:
            print()
            print(repr(BookDBM(**book)))
    
    print_get_books_page()
    command = input().strip()
    while command != "1":
        router.clear_console()
        if command == "2":
            router.print_centered(f"Найдено книг: {len(books)}")
            for book in books:
                print()
                print(repr(BookDBM(**book)))
        print_get_books_page()
        command = input().strip()
    router.clear_console()
    return BaseSchemaOut(status=200, result={
            "path": "/index_page", 
            "method": "GET",
            "body": None,
    })
    