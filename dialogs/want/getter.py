import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_item_metadata, new_order
from database import users

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

    # Getting data of item by Page in Users table
    item = await get_item_metadata(user_dict, db_engine)

    category = item['category']
    name = item['name']
    description = item['description']
    image = item['image']
    sell_price = item['sell_price']

    dialog_manager.current_context().dialog_data['current_count'] = item['count']

    logger.info(f'Item metadata for page:\n{name}\n{sell_price}')

    return {
        "button_back": i18n.button.back(),
        "button_take_it": i18n.button.take.it(),
        "button_account": i18n.button.account(),
        "button_catalogue": i18n.button.catalogue(),
        "item_info": i18n.item.show(
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


# Order confirmation
async def order_confirmation_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    new_order_data = dialog_manager.current_context().dialog_data

    page: int  # Current page of user from database

    # User data
    user_dict = dialog_manager.start_data
    username = user_dict['username']

    # Getting data of item from PAGE
    item = await get_item_metadata(user_dict, db_engine)

    category = item['category']
    name = item['name']
    description = item['description']
    image = item['image']
    sell_price = item['sell_price']

    dialog_manager.current_context().dialog_data['order_metadata'] = item

    return{
        "order_confirmation": i18n.confirm.new.order(
            username=username,
            address=new_order_data['address'],
            category=category,
            name=name,
            description=description,
            image=image,
            sell_price=sell_price,
            count=new_order_data['count'],
            total_sum=int(new_order_data['count']) * sell_price
        ),
        "button_confirm": i18n.button.confirm(),
        "button_back": i18n.button.back()
    }


# Complete order
async def complete_order_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    user_dict = dialog_manager.start_data
    new_order_data = dialog_manager.current_context().dialog_data

    await new_order(
        db_engine,
        i18n,
        user_dict,
        new_order_data
    )

    return {
        "order_complete": i18n.order.complete(),
        "button_take_it": i18n.take.it(),
        "button_catalogue": i18n.catalogue(),
        "button_account": i18n.account(),
        "button_back": i18n.back()
    }

