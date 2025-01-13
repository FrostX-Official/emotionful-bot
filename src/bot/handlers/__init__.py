from aiogram import Router

from . import start_menu, callback

def setup_routers() -> Router:
    router = Router()
    router.include_router(start_menu.router)
    router.include_router(callback.router)
    return router