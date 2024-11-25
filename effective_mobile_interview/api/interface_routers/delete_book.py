from time import sleep
from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut


router = CommandInterFaceRouter()

def print_delete_result_page():
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Вернуться на главную страницу")
    router.print_centered("2. Удалить книгу!")
    print("Действие номер: ", end="")

@router.get("/book/delete")
def delete_book_form():
    router.clear_console()
    router.print_centered("Введите id книги!")
    print("id книги: ", end="")
    try: 
        book_id = int(input())
    except:
        router.print_centered("Неверный формат id!")
        router.print_centered("Вы будете перемещены на главную страницу через 5 секунд!")
        sleep(5)
        return BaseSchemaOut(status=200, result={
            "path": "/index_page", 
            "method": "GET",
            "body": None,
        })
    
    return BaseSchemaOut(status=200, result={
        "path": "/book/delete/result", 
        "method": "POST",
        "api_url": f"/book.delete?book_id={book_id}",
        "api_method": "DELETE",
        "body": None})

@router.post("/book/delete/result")
def delete_book_result(
    is_done: bool
):
    if is_done:
        router.print_centered("Книга была успешно удалена!")
    else:
        router.print_centered("Книги с таким id не существует!")
    print_delete_result_page()
    command = input().strip()
    while command not in ["1", "2"]:
        router.clear_console()
        print_delete_result_page()
        command = input().strip()
    router.clear_console()
    if command == "1":
        return BaseSchemaOut(status=200, result={
                "path": "/index_page", 
                "method": "GET",
                "body": None,
        })
    return BaseSchemaOut(status=200, result={
            "path": "/book/delete", 
            "method": "GET",
            "body": None,
    })