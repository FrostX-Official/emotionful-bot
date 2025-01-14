"""
Handler loader for EmotionfulBot on Telegram.
Written by frostx-official on GitHub
"""

import logging

from aiogram import Router
from importlib import import_module
import os

def setup_routers() -> Router:
    router = Router()

    # What the fuck am I doing... 😭
    path = os.path.join(os.path.join(os.path.join(os.getcwd(), "src"), "bot"), "handlers")

    handlers = []
    for (_, _, filenames) in os.walk(path):
        handlers.extend(filenames)
        break

    for handler in handlers:
        if handler == "__init__.py" or not handler.endswith(".py"):
            continue

        handler = handler.split(".")[0]

        mdl = import_module(__package__+"."+handler)

        if not hasattr(mdl, "router"):
            logging.warning(f"Handler \"{handler}\" in bot.handlers doesn't have router! Handlers must include router in them for them to be loaded in bot.")
            continue

        router.include_router(mdl.router)

    return router