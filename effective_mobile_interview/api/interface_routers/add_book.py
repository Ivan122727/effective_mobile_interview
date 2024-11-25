from time import sleep
from effective_mobile_interview.api.schemas.book import CreateBookIn
from effective_mobile_interview.enumerations import BookStatus
from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut

def print_add_result_page():
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Вернуться на главную страницу")
    router.print_centered("2. Добавить еще одну книгу!")
    print("Действие номер: ", end="")

router = CommandInterFaceRouter()


@router.get("/book/add")
def add_book_form():
    router.clear_console()
    router.print_centered("Введите название книги!")
    print("Название книги: ", end="")
    title = input().strip()
    router.print_centered("Введите автора книги!")
    print("Автор: ", end="")
    author = input().strip()
    router.print_centered("Введите год издания!")
    print("Год издания: ", end="")
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
    book = CreateBookIn(title=str(title), author=author, year=year, book_status=BookStatus.AVAILABLE).to_doc()
    return BaseSchemaOut(status=200, result={
        "path": "/book/add/result", 
        "method": "POST",
        "api_url": "/book.add",
        "api_method": "POST",
        "body": {"book": book},
    })

@router.post("/book/add/result")
def result_add_book(is_done: bool):
    if is_done:
        router.print_centered("Книга успешно добавлена!")
    else:
        router.print_centered("Что-то пошло не так!")
    print_add_result_page()
    command = input().strip()
    while command not in ["1", "2"]:
        router.clear_console()
        print_add_result_page()
        command = input().strip()
    router.clear_console()
    if command == "1":
        return BaseSchemaOut(status=200, result={
                "path": "/index_page", 
                "method": "GET",
                "body": None,
        })
    return BaseSchemaOut(status=200, result={
            "path": "/book/add", 
            "method": "GET",
            "body": None,
            })