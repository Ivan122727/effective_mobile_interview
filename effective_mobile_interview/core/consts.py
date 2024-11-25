import os
import pathlib


BASE_DIRPATH = str(pathlib.Path(__file__).parent.parent.parent) # Путь к проекту
ENV_FILENAME: str = ".env" # Название env файла
ENV_FILEPATH: str = os.path.join(BASE_DIRPATH, ENV_FILENAME) # Путь к env файлу
STORAGE_DIRNAME: str = "storage" # Название дериктории, где хранится БД
STORAGE_DIRPATH: str = os.path.join(BASE_DIRPATH, STORAGE_DIRNAME) # Путь к хранилищу
