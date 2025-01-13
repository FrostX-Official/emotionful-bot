import logging

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from tortoise import Tortoise

from bot.handlers import setup_routers
from bot.middlewares import UserMiddleware
from config_reader import config

async def on_startup() -> None:
    logging.log(100, "Dispatcher Start")
    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models.user"]}
    )
    await Tortoise.generate_schemas()

async def on_shutdown() -> None:
    logging.log(100, "Dispatcher Shutdown")
    await Tortoise.close_connections()

async def main() -> None:
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    i18n = I18n(path="locales", default_locale="en", domain="messages")

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(setup_routers())
    dp.update.middleware(UserMiddleware())
    dp.update.middleware(SimpleI18nMiddleware(i18n))

    await bot.delete_webhook(True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    asyncio.run(main())