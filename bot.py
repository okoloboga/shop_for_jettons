import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from fluentogram import TranslatorHub

from config.config_reader import get_config, BotConfig, DbConfig
from config.config import Config, load_config
from handlers import unknown, buttons, switchers
from dialogs.start import start_dialog
from dialogs.account import account_dialog
from dialogs.want import want_dialog
from dialogs.catalogue import catalogue_dialog
from utils.i18n import TranslatorHub, create_translator_hub
from middlewares.i18n import TranslatorRunnerMiddleware
from database.tables import metadata
from services.ton_services import get_collection

logger = logging.getLogger(__name__)


# Configuration and boot Bot
async def main():

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting Bot')

    # Config
    db_config = get_config(DbConfig, "db")

    engine = create_async_engine(
        url=str(db_config.dsn),
        echo=db_config.is_echo
    )

    # Проверка соединения с СУБД
    async with engine.begin() as conn:
        # Выполнение обычного тектового запроса
        await conn.execute(text("SELECT 1"))

    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    config: Config = load_config()

    # Getting NFT collection
    await get_collection(engine)

    # Init Bot in Dispatcher
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(db_engine=engine)

    # i18n init
    translator_hub: TranslatorHub = create_translator_hub()

    # Routers, dialogs, middlewares
    dp.include_router(start_dialog)
    dp.include_router(account_dialog)
    dp.include_router(catalogue_dialog)
    dp.include_router(want_dialog)

    dp.include_router(buttons.router)
    dp.include_router(switchers.router)
    dp.include_router(unknown.router)
    dp.update.middleware(TranslatorRunnerMiddleware())

    setup_dialogs(dp)

    # Skipping old updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translator_hub=translator_hub)
    return bot

if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
