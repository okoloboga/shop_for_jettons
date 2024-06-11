import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from sqlalchemy import insert, delete, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from states.states import StartSG
from database.tables import users, catalogue

router = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

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
        .where(users.c.telegram_id==callback.from_user.id)
    )
    async with db_engine.connect() as conn:
        catalogue_len = await conn.execute(statement_len)
        user_page = await conn.execute(statement_page)
        logger.info(f'Catalogue len and user_page of {callback.from_user.id} is executed')

    catalogue_len = len(catalogue_len)
    logger.info(f'Catalogue len is {catalogue_len}')

    # Rewrite users page in database
    if user_page[0]==0:
        statement = (users.update()
                     .values(page=catalogue_len)
                     .where(users.c.telegram_id==callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {catalogue_len}')
    else:
        statement = (users.update()
                     .values(page=user_page[0]-1)
                     .where(users.c.telegram_id==callback.from_user.id))
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
        .where(users.c.telegram_id==callback.from_user.id)
    )
    async with db_engine.connect() as conn:
        catalogue_len = await conn.execute(statement_len)
        user_page = await conn.execute(statement_page)
        logger.info(f'Catalogue len and user_page of {callback.from_user.id} is executed')

    catalogue_len = len(catalogue_len)

    # Rewrite users page in database
    if user_page[0]==catalogue_len:
        statement = (users.update()
                     .values(page=0)
                     .where(users.c.telegram_id==callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {0}')
    else:
        statement = (users.update()
                     .values(page=user_page[0]+1)
                     .where(users.c.telegram_id==callback.from_user.id))
        async with db_engine.connect() as conn:
            await conn.execute(statement)
            await conn.commit()
            logger.info(f'User {callback.from_user.id} page changed to {user_page[0]+1}')

    await dialog_manager.switch_to(state=StartSG.start)
