from time import sleep
from effective_mobile_interview.enumerations import BookStatus
from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut


router = CommandInterFaceRouter()

def print_update_form_page():
    router.clear_console()
    router.print_centered("Выберите статус книги:")
    router.print_centered("1. В наличии")
    router.print_centered("2. Выдана")
    print("Статус: ", end="")

def print_update_result_page():
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Вернуться на главную страницу")
    router.print_centered("2. Обновить статус книги!")
    print("Действие номер: ", end="")

@router.get("/book/update")
def update_book_form():
    print_update_form_page()
    command = input().strip()
    while command not in ['1', '2']:
        print_update_form_page()
        command = input()
    book_status = BookStatus.AVAILABLE
    if command == "2":
        book_status = BookStatus.CHECKED_OUT
    router.print_centered("Введите id книги!")
    print("id книги: ", end="")
    try:
        book_id = int(input())
    except:
        router.print_centered("Неверный формат id книги!")
        router.print_centered("Вы будете перемещены на главную страницу через 5 секунд!")
        sleep(5)
        return BaseSchemaOut(status=200, result={
            "path": "/index_page", 
            "method": "GET",
            "body": None,
        })
    return BaseSchemaOut(status=200, result={
        "path": "/book/update/result",
        "method": "PATCH",
        "api_url": "/book.change_status",
        "api_method": "PATCH",
        "body": {"id": book_id, "book_status": book_status}
    })


@router.patch("/book/update/result")
def update_book_result(
    is_done: bool
):
    if is_done:
        router.print_centered("Статус книги успешно обновлен!")
    else:
        router.print_centered("Книга с таким id не найдена!")
    print_update_result_page()
    command = input().strip()
    while command not in ["1", "2"]:
        router.clear_console()
        print_update_result_page()
        command = input().strip()
    router.clear_console()
    if command == "1":
        return BaseSchemaOut(status=200, result={
                "path": "/index_page", 
                "method": "GET",
                "body": None,
        })
    return BaseSchemaOut(status=200, result={
            "path": "/book/update", 
            "method": "GET",
            "body": None,
            })