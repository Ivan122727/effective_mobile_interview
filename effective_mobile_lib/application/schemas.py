from typing import Any, Optional

from effective_mobile_lib.models.model import BaseModel


# class BaseSchemaOut:
#     """Базовая схеме ответа"""
#     def __init__(self, status: int, result: Any):
#         self.status = status
#         self.result = result

#     def __str__(self) -> str:
#         return str(self.result)

#     def __repr__(self) -> str:
#         res: dict[str, Optional[str]] = {'__class__': self.__class__.__name__}
#         for attr in vars(self):
#             res[attr] = getattr(self, attr)
#         return str(res)


class BaseSchemaIn(BaseModel):
    """Базовая схема входных данных"""
    ...


class BaseSchemaOut(BaseModel):
    """Базовая схема ответа"""
    status: int
    result: Any

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
