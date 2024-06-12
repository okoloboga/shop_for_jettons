import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import StartSG


router = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


"""Catalogue Switchers"""


# Item from catalogue selected
async def item_selection(
        callback: CallbackQuery,
        widget: Select,
        dialog_manager: DialogManager,
        item_id: str
):
    logger.info(f'User {callback.from_user.id} selected item {item_id} from catalogue')

    # Switcher to start dialog Window
    await dialog_manager.start(state=StartSG.show_item,
                               data={'item_id': item_id,
                                     'user_id': callback.from_user.id})


# Pressing on Previous Page button
async def previous_page(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    user_id = callback.from_user.id
    logger.info(f'User {user_id} pressed PREVIOUS PAGE')
    await dialog_manager.switch_to(state=StartSG.start_previous)


# Pressing on Next Page button
async def next_page(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    user_id = callback.from_user.id
    logger.info(f'User {user_id} pressed NEXT PAGE')
    await dialog_manager.switch_to(state=StartSG.start_next)
