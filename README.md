[Техническое задание](ТЗ.docx)
#### Нужно создать файл .env и поместить туда название файла с расширением .json
название env файла можно поменять в [Файл с различными константными перемеными](effective_mobile_interview/core/consts.py)
~~~
storage_filename=...
~~~
[Файл с настройками](effective_mobile_interview/core/settings.py)
#### Для старта приложения запустить main.py 
~~~
from effective_mobile_interview.core.application import start_app
from tests.insert_test_data import insert_test_data

if __name__ == "__main__":
    insert_test_data() # После первого запуска закомментируйте (для вставки тестовых данных, можно сразу закомментировать)
    start_app()
~~~
### Я написал для удобства модуль effective_mobile_lib
## Реализованная функциональность в модуле effective_mobile_lib
<ul>
    <li>Router - для обработки запросов</li>
    <li>Application - приложение</li>
    <li>BaseSettings - настройки проекта</li>
    <li>BaseModel - базовая модель с валидацией данных</li>
    <li>DB - база данных(Key-Value Store)</li>
    <li>CommandInterFaceRouter - Router для отображения страниц</li>
</ul>

## Реализованная функциональность согласно ТЗ
<hr>
<ul>
    <li> Добавление книги </li>
    <li>Удаление книги, проверка на существовение перед удалением</li>
    <li>Поиск книги: Пользователь может искать книги по title, author или year. По year у пользователя три варианта >, <, =</li>
    <li>Отображение всех книг</li>
    <li>Изменение статуса книги - валидация входных данных и проверка на существовение книги</li>
</ul>
<hr>

## Была разработана удобная структура, примером была структура в FastAPI фреймворке. 
