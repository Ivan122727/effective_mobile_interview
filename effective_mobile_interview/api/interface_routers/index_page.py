from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.schemas import BaseSchemaOut

router = CommandInterFaceRouter()

def print_index_page():
    router.clear_console()
    router.print_centered("Система учета библиотеки")
    router.print_centered("Выберите нужное действие:")
    router.print_centered("1. Добавить книгу")
    router.print_centered("2. Удалить книгу")
    router.print_centered("3. Найти книгу")
    router.print_centered("4. Отобразить все книги")
    router.print_centered("5. Изменить статус книги")
    router.print_centered("6. Завершить работу приложения")
    print("Действие номер: ", end="")

@router.get("/index_page")
def index_page():
    print_index_page()
    command = input().strip()
    while command not in ['1', '2', '3', '4', '5', '6']:
        print_index_page()
        command = input().strip()

    router.clear_console()
    if command == '1':
        return BaseSchemaOut(status=200, result={
            "path": "/book/add", 
            "method": "GET",
            "body": None,
            })
    elif command == '2':
        return BaseSchemaOut(status=200, result={
            "path": "/book/delete", 
            "method": "GET",
            "body": None,
            })
    elif command == '3':
        return BaseSchemaOut(status=200, result={
            "path": "/book/search", 
            "method": "GET",
            })
    elif command == '4':
        return BaseSchemaOut(status=200, result={
            "path": "/book/all", 
            "method": "POST",
            "api_url": "/book.get_all_books",
            "api_method": "GET",
            "body": None,
            })
    elif command == "5":
        return BaseSchemaOut(status=200, result={
            "path": "/book/update", 
            "method": "GET",
            "body": None,
            })
    else:
        return BaseSchemaOut(status=0, result={})
