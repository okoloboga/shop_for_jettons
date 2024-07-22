import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import new_item

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Start dialog of Add Row menu
async def add_row_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "add_row_main": i18n.add.row.main(),
        "button_add_row": i18n.button.add.row(),
        "button_back": i18n.button.back()
    }


# Switching to Fill Category
async def fill_category_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "fill_category": i18n.fill.category(),
        "button_back": i18n.button.back()
    }


# Switching to Fill Name
async def fill_name_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "fill_name": i18n.fill.name(),
        "button_back": i18n.button.back()
    }


# Switching to Fill Description
async def fill_description_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "fill_description": i18n.fill.description(),
        "button_back": i18n.button.back()
    }


# Switching to Fill Image URL
async def fill_image_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "fill_image": i18n.fill.image(),
        "button_back": i18n.button.back()
    }


# Switching to Fill Sell-price, Self-price and count of Item
async def fill_price_count_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):

    return {
        "fill_price_count": i18n.fill.price.count(),
        "button_back": i18n.button.back()
    }


# Offer to confirm new item
async def confirm_new_item_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    new_item_data = dialog_manager.current_context().dialog_data
    return {
        "confirm_new_item": i18n.confirm.new.item(
            category=new_item_data['category'],
            name=new_item_data['name'],
            description=new_item_data['description'],
            image=new_item_data['image'],
            sell_price=new_item_data['sell_price'],
            self_price=new_item_data['self_price'],
            count=new_item_data['count']
        ),
        "button_confirm": i18n.button.confirm(),
        "button_back": i18n.button.back()
    }


# Writing new item to database is complete
async def complete_new_item_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    logger.info(f'User {user_id} completing write new item')

    new_item_data = dialog_manager.current_context().dialog_data

    await new_item(
        db_engine,
        user_id,
        new_item_data
    )

    return {
        "item_complete": i18n.item.complete(),
        "button_add_row": i18n.button.add.row(),
        "button_back": i18n.button.back()
    }
