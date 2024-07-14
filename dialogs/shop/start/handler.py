import logging

from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import StartSG
from services import new_user
from database import users


router_start = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


'''Base Switchers'''


# Process START command
@router_start.message(CommandStart(deep_link_encoded=True))
async def command_start_process(
        message: Message,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
        command: CommandObject
) -> None:
    logger.info(f'==== Message: {message.text} ====')
    logger.info(f'==== Command.args: {command.args} ====')

    # If user start bot by referral link
    if command.args:
        logger.warning(f'CommandObject is {command}')
        args = command.args
        payload = decode_payload(args)
    else:
        payload = None
    user = []
    logger.info(f'Process START command from default state by user {message.from_user.id}\nPayload: {payload}')

    # Read users data from database
    statement = (
        select(column('wallet'), column('mnemonics'))
        .select_from(users)
        .where(users.c.telegram_id == message.from_user.id)
    )
    async with db_engine.connect() as conn:
        user_data = await conn.execute(statement)
        for row in user_data:
            user.append(row)
            logger.info(f'User data of {message.from_user.id} appended. Wallet: {user[0]}')

    # If User is New...
    if len(user) == 0:

        logger.warning(f'{message.from_user.id} is new user')
        wallet = await new_user(db_engine,
                                message.from_user.id,
                                message.from_user.first_name,
                                message.from_user.last_name,
                                payload)
        await dialog_manager.start(state=StartSG.start,
                                   data={'user_id': message.from_user.id},
                                   wallet={'wallet': wallet[0]},
                                   mnemonics={'mnemonics': wallet[1]}
                                   )
    else:
        logger.info(f'{message.from_user.id} is old user')
        await dialog_manager.start(state=StartSG.start,
                                   data={'user_id': message.from_user.id},
                                   wallet={'wallet': user[0]},
                                   mnemonics={'mnemonics': user[1]}
                                   )



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
