from effective_mobile_lib.application.application import Application
from .api.api_router import api_router
from .api.interface_router import interface_router


def create_app() -> Application:
    """Функция, создающая экземляр приложения

    Returns:
        Application: Приложение
    """
    app = Application()
    app.include_api_router(api_router)
    app.include_interface_router(interface_router)
    return app
