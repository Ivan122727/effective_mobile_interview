from functools import lru_cache
import os

from effective_mobile_interview.core.consts import BASE_DIRPATH, ENV_FILEPATH, STORAGE_DIRPATH
from effective_mobile_lib.models.settings import BaseSettings


class Settings(BaseSettings):
    """Класс Settings - настройки приложения"""
    storage_filename: str
    if not os.path.exists(STORAGE_DIRPATH):
            os.makedirs(STORAGE_DIRPATH, exist_ok=True)

    def __init__(self, _env_file: str = ".env", _env_file_encoding: str = "utf-8"):
        super().__init__(_env_file, _env_file_encoding)
        self.storage_filepath: str = os.path.join(STORAGE_DIRPATH, self.storage_filename)

@lru_cache()
def get_settings() -> Settings:
    """Функция, которая возвращает экземляр класса Settings
    Returns:
        Settings: Найстройки приложения
    """
    return Settings(_env_file=ENV_FILEPATH, _env_file_encoding="utf-8")
