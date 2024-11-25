from effective_mobile_lib.application.interface import CommandInterFaceRouter

from effective_mobile_interview.api.interface_routers.main_router import main_router

# Роутер для отрисовки данных
interface_router = CommandInterFaceRouter()
interface_router.include_router(main_router)