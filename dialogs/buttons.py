import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from states import StartSG, AccountSG, CatalogueSG, WantSG
from database import users, catalogue

router_buttons = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

"""Default handlers"""


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


# Switch to Account dialogue
async def switch_to_account(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Account dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=AccountSG.account,
                               data={'user_id': callback.from_user.id}
                               )


# Switch to Catalogue dialog
async def switch_to_catalogue(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Catalogue dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=CatalogueSG.catalogue)


# Switch to Want dialogue
async def switch_to_want(
        callback: CallbackQuery,
        dialog_manager: DialogManager
):
    logger.info(f'Switch to Want dialog by user {callback.from_user.id}')
    await dialog_manager.start(state=WantSG.want,
                               data={
                                   'user_id': callback.from_user.id,
                                   'username': callback.from_user.username
                                }
                               )


# Process BACK button
async def go_back(callback: CallbackQuery,
                  db_engine: AsyncEngine,
                  button: Button,
                  dialog_manager: DialogManager):

    # Get len of catalogue and current users page
    statement_len = (
        select(column("index"))
        .select_from(catalogue)
    )
    statement_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == callback.from_user.id)
    )
    async with db_engine.connect() as conn:
        catalogue_len = await conn.execute(statement_len)
        user_page = await conn.execute(statement_page)
        logger.info(f'Catalogue len and user_page of {callback.from_user.id} is executed')

    catalogue_len = len(catalogue_len)
    logger.info(f'Catalogue len is {catalogue_len}')

    # Rewrite users page in database
    if user_page[0] == 0:
        statement = (users.update()
                     .values(page=catalogue_len)
                     .where(users.c.telegram_id == callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {catalogue_len}')
    else:
        statement = (users.update()
                     .values(page=user_page[0]-1)
                     .where(users.c.telegram_id == callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {user_page[0]-1}')

    await dialog_manager.switch_to(state=StartSG.start)


# Process NEXT button
async def go_next(callback: CallbackQuery,
                  db_engine: AsyncEngine,
                  button: Button,
                  dialog_manager: DialogManager):

    # Get len of catalogue and current users page
    statement_len = (
        select(column("index"))
        .select_from(catalogue)
    )
    statement_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == callback.from_user.id)
    )
    async with db_engine.connect() as conn:
        catalogue_len = await conn.execute(statement_len)
        user_page = await conn.execute(statement_page)
        logger.info(f'Catalogue len and user_page of {callback.from_user.id} is executed')

    catalogue_len = len(catalogue_len)

    # Rewrite users page in database
    if user_page[0] == catalogue_len:
        statement = (users.update()
                     .values(page=0)
                     .where(users.c.telegram_id == callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {0}')
    else:
        statement = (users.update()
                     .values(page=user_page[0]+1)
                     .where(users.c.telegram_id == callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {user_page[0]+1}')

    await dialog_manager.switch_to(state=StartSG.start)
