from functools import wraps
from inspect import signature, Parameter
from typing import Any, Union, get_origin, get_args

from effective_mobile_lib.helpers import try_convert
from .schemas import BaseSchemaOut

class Router:
    def __init__(self):
        self.routes = []

    def route(self, path: str, method: str) -> BaseSchemaOut:
        """Декоратор для добавления роутов

        Args:
            path (str): Путь
            method (str): Метод

        Returns:
            BaseSchemaOut: Response
        """
        def inner(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # получаем данные из body и query
                bound_args = signature(func).bind_partial()
                query = kwargs.get('query', {})
                bound_args.arguments.update(query)
                body = kwargs.get('body', {})

                if method in ['POST', 'PUT', 'PATCH']:
                    if not body:
                        return BaseSchemaOut(status=400, result=f"Body is required for {method} requests")
                    bound_args.arguments.update(body)
                elif method in {'GET', 'DELETE'} and body:
                    return BaseSchemaOut(status=400, result=f"Body is not allowed for {method} requests")
                # Валидация и конвертация данных
                annotations = func.__annotations__
                for param_name, param_value in bound_args.arguments.items():
                    if param_name not in annotations:
                        return BaseSchemaOut(status=422, result=f"Invalid parameter '{param_name}'")
                
                for param_name, param_type in annotations.items():
                    if param_name in bound_args.arguments:
                        value = bound_args.arguments[param_name]
                        try:
                            bound_args.arguments[param_name] = try_convert(value, param_type)
                        except Exception as e:
                            return BaseSchemaOut(status=422, result=str(e))
                    else:
                        param = signature(func).parameters.get(param_name)
                        if param and param.default is not Parameter.empty:
                            try:
                                bound_args.arguments[param_name] = try_convert(param.default, param_type)
                            except Exception as e:
                                return BaseSchemaOut(status=422, result=str(e))
                        elif get_origin(param_type) is Union and type(None) in get_args(param_type):
                            bound_args.arguments[param_name] = None
                        else:
                            return BaseSchemaOut(status=422, result=f"Missing required parameter '{param_name}'.")
                res: BaseSchemaOut = func(**bound_args.arguments)
                return res

            self.routes.append({
                'path': path, 'method': method, 'func': wrapper
            })
            return wrapper
        return inner

    def get(self, path: str):
        return self.route(path, 'GET')

    def post(self, path: str):
        return self.route(path, 'POST')

    def put(self, path: str):
        return self.route(path, 'PUT')

    def patch(self, path: str):
        return self.route(path, 'PATCH')
    
    def delete(self, path: str):
        return self.route(path, 'DELETE')

    def include_router(self, router: 'Router'):
        for route in router.routes:
            self.routes.append(route)
