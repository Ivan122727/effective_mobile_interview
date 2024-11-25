from copy import deepcopy
from datetime import datetime
import json
import re
from typing import Any

from effective_mobile_lib.models.model import Document
from .base import BaseFields


class DB:
    def __init__(self, storage_filepath: str):
        """Инициализация класс и загрузка данных из json
        Args:
            storage_filepath (str): путь к json файлу
        """
        self.storage_filepath: str = storage_filepath
        try:
            with open(storage_filepath, 'r', encoding="utf-8") as storage_file:
                content = storage_file.read().strip()
                if content:
                    self.db: dict[str, Document] = json.loads(content)
                else:
                    self.db = {}
        except FileNotFoundError:
            self.db = {}
        self.ensure_indexes()
        self.count_docs = len(self.db[BaseFields.id])
        self.db["id_last_elem"] = int(self.db.get("id_last_elem", 0))
        self.save()

    def create_index(self, attr: str):
        """Создание индекса для поиска"""
        if attr in self.indexes:
            return
        self.db[attr] = {}
        if self.indexes:
            index = self.indexes[0]
            for obj in self.db[index]:
                doc: dict = deepcopy(self.db[index][obj])
                doc[index] = obj
                key = doc.pop(attr)
                self.db[attr][key] = doc
        self.indexes.append(attr)
        self.save()

    def ensure_indexes(self):
        """Создание индексов"""
        self.indexes: list[str] = list(self.db.keys() - {"id_last_elem"})
        if not self.indexes:
            self.create_index(BaseFields.id)

    def insert_document(self, doc: Document) -> int:
        """Метод вставки документа

        Args:
            doc (Document): Данные

        Returns:
            int: id документа
        """
        doc[BaseFields.created] = str(datetime.now())
        for index in self.indexes:
            if index in doc:
                obj = deepcopy(doc)
                key = obj.pop(index)
                obj[BaseFields.id] = str(self.db["id_last_elem"])
                self.db[index][key] = obj

        self.db[BaseFields.id][str(self.db["id_last_elem"])] = deepcopy(doc)
        self.count_docs += 1
        self.db["id_last_elem"] += 1
        self.save()
        return self.db["id_last_elem"] - 1

    def delete_document(self, doc_index: str, doc_key: str) -> bool:
        """Метод для удаление документа из БД

        Args:
            doc_index (str): индекс для поиска
            doc_key (str): значение для этого индекса

        Returns:
            bool: Статус операции
        """
        doc: Document = deepcopy(self.find_by_index(doc_index, str(doc_key)))
        doc[doc_index] = str(doc_key)
        was_deleted = False
        for index, key in doc.items():
            if index in self.db and key in self.db[index]:
                del self.db[index][key]
                was_deleted = True
        self.count_docs -= was_deleted
        self.save()
        return was_deleted

    def find_by_index(self, index: str, key: str) -> Document:
        """Метод поиска по индексу

        Args:
            index (str): Индекс для поиска
            key (str): Значение

        Returns:
            Document: Документ
        """
        doc: dict = deepcopy(self.db.get(index, {}).get(str(key), None))
        if doc:
            doc[index] = str(key)
        return doc

    def update_by_index(self, index: str, key: str, set_: Document):
        """Мето обновления по индексу

        Args:
            index (str): Индекс для поиска
            key (str): Значение
            set_ (Document): Данные которые нужно установить

        Returns:
            _type_: статус операции
        """
        was_updated = False
        if index not in self.indexes:
            return was_updated
        doc: Document = self.find_by_index(index, str(key))
        if not doc:
            return was_updated
        # # Получаем недостающие параметры
        for attr, value in doc.items():
            if attr not in set_:
                set_[attr] = deepcopy(value)
        # # Если есть лишние параметры
        for attr, value in set_.items():
            if attr not in doc:
                return was_updated
        # # Проверка если меняем значение для параметра с индексом на совпадение id
        for db_index in self.indexes:
            founded_doc = deepcopy(self.find_by_index(db_index, set_[db_index]))
            if founded_doc and founded_doc[BaseFields.id] != doc[BaseFields.id]:
                return was_updated
        # # Обновляем БД
        for db_index in self.indexes:
            obj = deepcopy(set_)
            key = obj.pop(db_index)
            self.db[db_index][key] = obj
        self.save()
        return was_updated     

    def get_all_items(self) -> list[Document]:
        """Метод возвращающий все документы БД

        Returns:
            list[Document]: Документы
        """
        list_elems: list[Document] = list()
        for key, value in self.db[BaseFields.id].items():
            obj = deepcopy(value)
            obj[BaseFields.id] = key
            list_elems.append(obj)
        return list_elems

    def drop_database(self):
        """Метод для очистки БД"""
        self.db = dict()
        self.indexes = list()
        self.create_index(BaseFields.id)
        self.count_docs = 0
        self.db["id_last_elem"] = 0
        self.save()

    def search_docs(self, expression: str, field: str) -> list[Document]:
        """Метод поиска значение

        Args:
            expression (str): Выражение
            field (str): Атрибут по которому ищем

        Returns:
            list[Document]: Найденеые документы
        """
        results = []
        if re.match(r'^>\s*-?\d+$', expression):
            value = int(expression[1:].strip())
            results = [val for val in self.get_all_items() if int(val[field]) > value]
        elif re.match(r'^<\s*-?\d+$', expression):
            value = int(expression[1:].strip())
            results = [val for val in self.get_all_items() if int(val[field]) < value]
        elif re.match(r'^=\s*-?\d+$', expression):
            value = int(expression[1:].strip())
            results = [val for val in self.get_all_items() if int(val[field]) == value]
        else:
            pattern = re.compile(re.escape(expression), re.IGNORECASE)
            results = [val for val in self.get_all_items() if pattern.search(str(val[field]))]
        return results

    def save(self):
        """Сохранение данных в файл"""
        with open(self.storage_filepath, 'w', encoding="utf-8") as storage_file:
            json.dump(self.db, storage_file, indent=4)
