from typing import Any, Iterator, Optional, Tuple
from effective_mobile_lib.helpers import try_convert

Document = dict[str, Any]

class BaseModel:
    @classmethod
    def get_combined_annotations(cls) -> dict[str, Any]:
        """Функция для получение комбинированной аннотации текущего класса и родительских

        Returns:
            dict[str, Any]: комбинированная аннотация
        """
        annotations = {}
        for base in cls.mro():
            annotations.update(getattr(base, '__annotations__', {}))
        return annotations
    
    def __init__(self, **kwargs) -> None:
        """Метод для инициализации класса и валидации данных"""
        annotations = self.get_combined_annotations()
        # Поиск лишних атрибутов
        for attr in kwargs.keys():
            if attr not in annotations:
                raise Exception(f"Invalid attribute '{attr}'")
        # Валидация полученных аттрибутов
        for attr, type_attr in annotations.items():
            if attr in kwargs:
                try:
                    setattr(self, attr, try_convert(kwargs[attr], type_attr))
                except ValueError as e:
                    raise ValueError(f"Error converting attribute '{attr}': {e}")
            else:
                default_value = getattr(self.__class__, attr, None)
                if default_value is not None:
                    try:
                        setattr(self, attr, try_convert(default_value, type_attr))
                    except ValueError as e:
                        raise ValueError(f"Error converting default value for attribute '{attr}': {e}")
                else:
                    raise Exception(f"Missing required attribute '{attr}'")

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        res: dict[str, Optional[str]] = {'__class__': self.__class__.__name__}
        for attr in vars(self):
            res[attr] = getattr(self, attr)
        return str(res)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for attr in vars(self):
            yield attr, getattr(self, attr)

    def keys(self) -> Iterator[str]:
        for attr in vars(self):
            yield attr

    def items(self) -> Iterator[Tuple[str, Any]]:
        for attr in vars(self):
            yield attr, getattr(self, attr)

    def __getitem__(self, attr: str) -> Any:
        return getattr(self, attr)

    def __setitem__(self, attr: str, value: Any) -> None:
        annotations = self.get_combined_annotations()
        if attr not in annotations:
            raise Exception(f"Invalid attribute '{attr}'")
        try:
            setattr(self, attr, try_convert(value, annotations[attr]))
        except ValueError as e:
            raise ValueError(f"Error converting attribute '{attr}': {e}")
    
    def to_doc(self) -> Document:
        return {attr: getattr(self, attr) for attr in self.get_combined_annotations()}