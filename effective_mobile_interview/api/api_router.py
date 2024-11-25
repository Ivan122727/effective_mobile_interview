from effective_mobile_lib.application.router import Router
from .api_routers.book import api_router as book_api_router

# Роутер для обработки API запросов
api_router = Router()
api_router.include_router(book_api_router)
