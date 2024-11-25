from typing import Any, Iterator, Optional, Tuple
from datetime import datetime

from effective_mobile_lib.helpers import try_convert
from .helpers import SetForClass
from effective_mobile_lib.models.model import BaseModel


class BaseFields(SetForClass):
    """Базовые поля документа в БД"""
    id: str = "id"
    created: str = "created"


class BaseDBM(BaseModel):
    """Базовая модель документя в БД"""
    id: int
    created: str

