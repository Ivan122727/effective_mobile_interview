from typing import Any, Union, Optional, get_origin, get_args


def try_convert(value, target_type):
    """Функция приведения к типу
    Args:
        value (_type_): Значение переменной
        target_type (_type_): Тип к которому нужно привести
    Raises:
        ValueError: Ошибка приведения

    Returns:
        _type_: Приведеное значение
    """
    if target_type is Any:
        return value
    elif isinstance(value, dict):
        return target_type(**value)
    elif get_origin(target_type) is Union:
        for type_ in get_args(target_type):
            try:
                return type_(value)
            except (ValueError, TypeError):
                continue
        raise ValueError(f"Invalid type for value '{value}'. Expected one of {get_args(target_type)}.")
    elif get_origin(target_type) is Optional:
        if value is None:
            return None
        type_ = get_args(target_type)[0]
        try:
            return type_(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid type for value '{value}'. Expected {type_.__name__}.")
    else:
        try:
            return target_type(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid type for value '{value}'. Expected {target_type.__name__}.")
