import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Select

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import StartSG


router_catalogue = Router()

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


# Process START command from another states
async def go_start(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
) -> None:
    logger.info(f'Process START command from non-default state by user {callback.from_user.id}')
    await dialog_manager.start(state=StartSG.start,
                               mode=StartMode.RESET_STACK,
                               data={'user_id': callback.from_user.id}
                               )
