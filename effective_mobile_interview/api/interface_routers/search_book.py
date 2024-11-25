import sys
from time import sleep
from xml.dom.minidom import Document
from effective_mobile_interview.db.collections.book import BookDBM
from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut


def print_search_books_page():
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Вернуться на главную страницу")
    router.print_centered("2. Найти книгу!")
    print("Действие номер: ", end="")

router = CommandInterFaceRouter()

def print_param_page():
    router.clear_console()
    router.print_centered("Выберите параметр по которому будете искать!")
    router.print_centered("1. Название книги")
    router.print_centered("2. Автор книги")
    router.print_centered("3. Год издания книги")
    print("Параметр: ", end="")

def print_year_page():
    router.print_centered("Выберите параметр по которому будете искать!")
    router.print_centered("1. Изданные позднее этого года")
    router.print_centered("2. Изданные раннее этого года")
    router.print_centered("3. Изданные в этот год")
    print("Параметр: ", end="")

@router.get("/book/search")
def search_book():
    print_param_page()
    command = input().strip()
    while command not in ['1', '2', '3']:
        print_param_page()
        command = input()
    api_url = str()
    if command == "1":
        router.print_centered("Введите название книги!")
        print("Название книги: ", end="")
        title = input()
        api_url = f"/book.search_by_title?expression={title}".strip()
    elif command == "2":
        router.print_centered("Введите автора книги!")
        print("Автор книги: ", end="")
        author = input()
        api_url = f"/book.search_by_author?expression={author}".strip()
    else:
        print_year_page()
        command = input()
        while command not in ['1', '2', '3']:
            print_year_page()
            command = input()
        if command == "1":
            expression = ">"
        elif command == "2":
            expression = "<"
        else:
            expression = "="     
        router.print_centered("Введите год!")
        print("Год: ", end="")
        try:
            year = int(input())
        except:
            router.print_centered("Неверный формат года издания!")
            router.print_centered("Вы будете перемещены на главную страницу через 5 секунд!")
            sleep(5)
            return BaseSchemaOut(status=200, result={
                "path": "/index_page", 
                "method": "GET",
                "body": None,
            })
        api_url =  f"/book.search_by_year?expression={expression}{year}"
    return BaseSchemaOut(status=200, result={
        "path": "/book/search/result",
        "method": "POST",
        "body": None,
        "api_url": api_url,
        "api_method": "GET"
    })

@router.post("/book/search/result")
def search_book_result(
    books: list[Document]
):
    if len(books) == 0:
        router.print_centered("Книг по таким параметрам не найдено!")
    else:
        router.print_centered(f"Найдено книг: {len(books)}")
    for book in books:
            print()
            print(repr(BookDBM(**book)))

    print_search_books_page()
    command = input().strip()
    while command not in ["1", "2"]:
        router.clear_console()
        print_search_books_page()
        command = input().strip()
    router.clear_console()
    if command == "1":
        return BaseSchemaOut(status=200, result={
                "path": "/index_page", 
                "method": "GET",
                "body": None,
        })
    return BaseSchemaOut(status=200, result={
            "path": "/book/search", 
            "method": "GET",
    })
    