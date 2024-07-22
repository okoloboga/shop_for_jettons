import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import *


router_admin_start = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Process START command from another states
async def go_start(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Process START command from non-default state by user {callback.from_user.id}')
    await dialog_manager.start(state=Admin_StartSG.main,
                               mode=StartMode.RESET_STACK,
                               data={'user_id': callback.from_user.id}
                               )
    

# Process START command from from main Admin menu
async def go_start_total(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Process START command from non-default state by user {callback.from_user.id}')
    await dialog_manager.start(state=StartSG.start,
                               mode=StartMode.RESET_STACK,
                               data={'user_id': callback.from_user.id}
                               )


# Switch to Catalogue dialog
async def switch_to_catalogue(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Catalogue dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=Admin_CatalogueSG.catalogue,
                               data={'user_id': callback.from_user.id})


# Switch to Add Row dialog
async def switch_to_add_row(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Add Row dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=AddRowSG.add_row,
                               data={'user_id': callback.from_user.id})


# Switch to Edit Row dialog
async def switch_to_edit_row(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Edit Row dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=EditRowSG.edit_row,
                               data={'user_id': callback.from_user.id})


# Switch to Confirm Order dialog
async def switch_to_confirm_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
        logger.info(f'Switch to Confirm Order dialog by user {callback.from_user.id}')
        await dialog_manager.start(state=ConfirmOrderSG.select_status,
                                   data={'user_id': callback.from_user.id})

