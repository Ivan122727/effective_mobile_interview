from effective_mobile_interview.api.schemas.book import CreateBookIn
from effective_mobile_interview.db.library_db import db
from effective_mobile_interview.enumerations import BookStatus

books = [
    CreateBookIn(title="War and Peace", author="Leo Tolstoy", year=1869, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Anna Karenina", author="Leo Tolstoy", year=1878, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Crime and Punishment", author="Fyodor Dostoevsky", year=1866, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="The Idiot", author="Fyodor Dostoevsky", year=1869, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="The Brothers Karamazov", author="Fyodor Dostoevsky", year=1880, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Eugene Onegin", author="Alexander Pushkin", year=1833, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="The Captain's Daughter", author="Alexander Pushkin", year=1836, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Dead Souls", author="Nikolai Gogol", year=1842, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="The Government Inspector", author="Nikolai Gogol", year=1836, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Fathers and Sons", author="Ivan Turgenev", year=1862, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Home of the Gentry", author="Ivan Turgenev", year=1859, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="A Hero of Our Time", author="Mikhail Lermontov", year=1840, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="The Master and Margarita", author="Mikhail Bulgakov", year=1966, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Doctor Zhivago", author="Boris Pasternak", year=1957, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="And Quiet Flows the Don", author="Mikhail Sholokhov", year=1940, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Oblomov", author="Ivan Goncharov", year=1859, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Woe from Wit", author="Alexander Griboyedov", year=1825, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Demons", author="Fyodor Dostoevsky", year=1872, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Poor Folk", author="Fyodor Dostoevsky", year=1846, book_status=BookStatus.AVAILABLE),
    CreateBookIn(title="Childhood", author="Leo Tolstoy", year=1852, book_status=BookStatus.AVAILABLE),
]

def insert_test_data():
    """Функция, которая вставляет тестовые данные"""
    db.drop_database()
    for book in books:
        db.insert_document(book.to_doc())
