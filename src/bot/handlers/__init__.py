from aiogram import Router

from . import start_menu, unimplemented, stars_donation

def setup_routers() -> Router:
    router = Router()
    router.include_router(start_menu.router)
    router.include_router(unimplemented.router)
    router.include_router(stars_donation.router)
    return router