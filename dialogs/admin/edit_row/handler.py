import logging

from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input.text import ManagedTextInput

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from fluentogram import TranslatorRunner

from states import StartSG, CatalogueSG, AddRowSG, EditRowSG


router_edit_row = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Edit Item process - Start
async def edit(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} starts editing item')
    await dialog_manager.switch_to(EditRowSG.edit)


# Delete Item process
async def delete(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} starts delete item')
    await dialog_manager.switch_to(EditRowSG.delete)


# Delete confirmed
async def delete_confirm(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} delete item')
    await dialog_manager.switch_to(EditRowSG.delete_confirmed)


# Filling changes confirmed
async def fill_changes(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        new_data: list
):
    logger.info(f'User {callback.from_user.id} filled changes: {new_data}')

    dialog_manager.current_context().dialog_data['new_data'] = new_data
    await dialog_manager.switch_to(EditRowSG.changes_confirmed)


# Wrong changes
async def wrong_changes(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        new_data: str
):
    logger.warning(f'User {callback.from_user.id} fills wrong changes')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.changes())


















