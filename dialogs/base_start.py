import logging

from aiogram import Router, F
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from redis import asyncio as aioredis
from fluentogram import TranslatorRunner
from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import FSMMain, StartSG
from services import new_user
from database import users, new_user_template
from states import AccountSG, WantSG
from .buttons import start_kb
from .game import play_account_kb

router_base_start = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Process START command
@router_base_start.message(CommandStart(deep_link_encoded=True))
async def command_start_process(
        message: Message,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
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
        select("*")
        .select_from(users)
        .where(users.c.telegram_id == message.from_user.id)
    )
    async with db_engine.connect() as conn:
        user_data = await conn.execute(statement)
        logger.info(f'User data of {message.from_user.id} is executed')

    for row in user_data:
        user.append(row)
        logger.info(f'User data of {message.from_user.id} appended: {user[0]}')

    # If User is New...
    if len(user) == 0:

        logger.warning(f'{message.from_user.id} is new user')
        await new_user(db_engine,
                       message.from_user.id,
                       message.from_user.first_name,
                       message.from_user.last_name,
                       payload)
        await message.answer(text=i18n.base.start(),
                             reply_markup=start_kb(i18n))
    else:
        logger.info(f'{message.from_user.id} is old user')
        await message.answer(text=i18n.base.start(),
                             reply_markup=start_kb(i18n))
        

# Processing Shop button
@router_base_start.callback_query(F.data == 'shop')
async def start_shop_process(callback: CallbackQuery,
                             dialog_manager: DialogManager
):
    await dialog_manager.start(state=StartSG.start,
                               data={'user_id': callback.from_user.id}
                               )

# Processing Game button
@router_base_start.callback_query(F.data == 'game')
async def start_game_process(callback: CallbackQuery,
                             state: FSMContext,
                             dialog_manager: DialogManager
                             ):
    logger.info(f'User {callback.from_user.id} enter the Game')
    r = aioredis.Redis(host='localhost', port=6379)
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    # User first time in bot - add him to DB
    if await r.exists(str(callback.from_user.id)) == 0:
        await r.hmset(str(callback.from_user.id), new_user_template)
    await callback.message.answer(text=i18n.chose.action(),
                          reply_markup=play_account_kb(i18n))
    await state.set_state(FSMMain.main)