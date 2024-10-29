import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import create_async_engine
from fluentogram import TranslatorHub

from config import get_config, BotConfig, DbConfig
from dialogs import (shop_dialogs, shop_routers, game_routers, game_dialogs, admin_dialogs,
                     admin_routers, router_unknown)
from utils import TranslatorHub, create_translator_hub
from middlewares import TranslatorRunnerMiddleware
from database import metadata
from services import get_admins_list

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
        echo=False
    )

    # Create Tables
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    # Init Bot in Dispatcher
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(db_engine=engine)

    # i18n init
    translator_hub: TranslatorHub = create_translator_hub()

    # Routers, dialogs, middlewares
    dp.include_routers(*shop_dialogs, *shop_routers, game_dialogs, *game_routers,
                       *admin_dialogs, *admin_routers)
    dp.include_router(router_unknown)

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.workflow_data.update({'admins': await get_admins_list(engine)})

    setup_dialogs(dp)
 
    # Skipping old updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _translator_hub=translator_hub)
    return bot

if __name__ == '__main__':
    asyncio.run(main())
