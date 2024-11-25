from urllib.parse import parse_qs, urlparse

from effective_mobile_lib.application.interface import CommandInterFaceRouter
from effective_mobile_lib.application.router import Router
from .schemas import BaseSchemaOut

class Application:
    def __init__(self, api_router: Router = Router(), interface_router: CommandInterFaceRouter = CommandInterFaceRouter()):
        self.api_router = api_router
        self.interface_router = interface_router

    def include_api_router(self, router: Router):
        """Добавление роутов из роутера

        Args:
            router (Router): Роутер
        """
        for route in router.routes:
            self.api_router.routes.append(route)

    def include_interface_router(self, router: CommandInterFaceRouter):
        for route in router.routes:
            self.interface_router.routes.append(route)

    def _process_request(self, router: Router, path: str, method: str = None, body: dict = None) -> BaseSchemaOut:
        """Метод обработки запроса

        Args:
            router (Router): Роутер
            path (str): Path
            method (str, optional): Метод запроса
            body (dict, optional): Тело запроса

        Returns:
            BaseSchemaOut: Response
        """
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        query = {k: v[0] for k, v in query_params.items()}
        # print(f"{method} {path}")
        for route in router.routes:
            if route['path'] == parsed_url.path and route['method'] == method:
                func = route['func']
                return func(body=body, query=query)
        return BaseSchemaOut(status=404, result="Route not found")

    def process_api_request(self, path: str, method: str, body: dict = None) -> BaseSchemaOut:
        return self._process_request(self.api_router, path, method, body)

    def process_interface_request(self, path: str, method: str, body: dict = None) -> BaseSchemaOut:
        return self._process_request(self.interface_router, path, method, body=body)

def __example__():
    router = Router()

    @router.get("/example")
    def example(age: int):
        return {"status": 200, "result": age}

    app = Application(router)

    print(app._process_request("/example?age=12", "GET"))
