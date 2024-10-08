import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from states import StartSG


router_catalogue = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


"""Catalogue Switchers"""


# Item from catalogue selected
async def item_selection(callback: CallbackQuery,
                         widget: Select,
                         dialog_manager: DialogManager,
                         item_id: str):
                         
    logger.info(f'User {callback.from_user.id} selected item {item_id} from catalogue')

    # Switcher to start dialog Window
    await dialog_manager.start(state=StartSG.show_item,
                               data={'item_id': item_id,
                                     'user_id': callback.from_user.id})

