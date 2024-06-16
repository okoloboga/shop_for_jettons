import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_item_metadata
from database import users, catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show more information about item
async def item_info_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    page: int  # Current page of user from database

    # User ID
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    # Get current page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')

    # Getting data of item from PAGE
    item = await get_item_metadata(int(page), db_engine)

    category = item['category']
    name = item['name']
    description = item['description']
    image = item['image']
    sell_price = item['sell_price']

    logger.info(f'Item metadata for page:\n{name}\n{sell_price}')

    return {
        "button_back": i18n.button.back(),
        "button_take_it": i18n.button.take.it(),
        "button_account": i18n.button.account(),
        "button_catalogue": i18n.button.catalogue(),
        "item_show": i18n.item.show(
            category=category,
            name=name,
            description=description,
            sell_price=sell_price
        ),
        "image": image
    }


# Switching to Fill count
async def fill_count_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

    return {
        "fill_count": i18n.fill.count(),
        "button_back": i18n.button.back()
    }


# Switching to Fill count
async def fill_address_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

    return {
        "fill_address": i18n.fill.address(),
        "button_back": i18n.button.back()
    }


# Buying confirmation
async def buy_confirmation(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

