
import os
from typing import Union, get_args, get_origin

from .model import BaseModel


class BaseSettings(BaseModel):
    def __init__(self, _env_file: str = ".env", _env_file_encoding: str = "utf-8") -> None:
        """Инициализация класса базовых настройк

        Args:
            _env_file (str, optional): Название env файла. Значение по умолчанию ".env".
            _env_file_encoding (str, optional): Кодировка файла. Defaults to "utf-8".
        """
        self._env_file = _env_file
        self._env_file_encoding = _env_file_encoding
        self._load_env_file()

    def _load_env_file(self) -> None:
        """Метод для загрузки данных с env файла"""
        try:
            with open(file=self._env_file, mode='r', encoding=self._env_file_encoding) as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip('"').strip("'")
        except FileNotFoundError:
            raise Exception(f"File {self._env_file} not found.")
        except Exception as e:
            raise Exception(f"Error loading {self._env_file}: {e}")
        for attr, type_attr in self.__class__.__annotations__.items():
            value = os.getenv(attr)
            if value is not None:
                if get_origin(type_attr) is Union:
                    types = get_args(type_attr)
                    for t in types:
                        if t is not type(None):
                            setattr(self, attr, t(value))
                            break
                else:
                    setattr(self, attr, type_attr(value))
            else:
                default_value = getattr(self.__class__, attr, None)
                if default_value is not None:
                    setattr(self, attr, default_value)
                elif get_origin(type_attr) is Union and type(None) in get_args(type_attr):
                    setattr(self, attr, default_value)
                else:
                    raise ValueError(f"Missing required environment variable: {attr}")


    