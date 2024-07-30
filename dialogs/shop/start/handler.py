import logging
import pprint

from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode

from fluentogram import TranslatorRunner
from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from redis import asyncio as aioredis

from services.ton_services import central_check
from states import StartSG
from services import new_user, central_check
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
    logger.info(f'==== command: {command} ====')
    logger.info(f'==== Command.args: {command.args} ====')
    
    r = aioredis.Redis(host='localhost', port=6379)

    # If user start bot by referral link
    if command.args:
        logger.info(f'CommandObject is {command}')
        args = command.args
        payload = decode_payload(args)
    else:
        payload = None
    user = []
    logger.info(f'Process START command from default state by user {message.from_user.id}\nPayload: {payload}')

    # Read users data from database
    statement = (
        select(column('address'), column('mnemonics'))
        .select_from(users)
        .where(users.c.telegram_id == message.from_user.id)
    )
    async with db_engine.connect() as conn:
        user_data = await conn.execute(statement)
        for row in user_data:
            user.append(row[0])
            user.append(row[1])
            logger.info(f'User {message.from_user.id} data is loaded.\
                        \nWallet is {row[1]}')

    # If User is New...
    if len(user) == 0:
    
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

        # Central wallet has enough TON for deploy new wallet?
        if await central_check():
            await message.answer(text=i18n.hello())
            
            logger.warning(f'{message.from_user.id} is new user')
            wallet_data = await new_user(db_engine,
                                         message.from_user.id,
                                         message.from_user.first_name,
                                         message.from_user.last_name,
                                         payload)
            
            # User first time in Redis DB - add him to DB      
            new_user_template = {
                'total_games': 0,
                'win': 0,
                'lose': 0,
                'rating': 0,
                'current_game': 0,
                'last_message': 0,
                'wallet': wallet_data[0],
                'mnemonics': wallet_data[1]
                }
                
            await r.hmset(str(message.from_user.id), new_user_template)
                
            logger.info(f'User {message.from_user.id} is New.\
                Added to Redis\n{pprint.pprint(new_user_template)}')
            
            await dialog_manager.start(state=StartSG.start,
                                       mode=StartMode.RESET_STACK,
                                       data={'user_id': message.from_user.id}
                                       )
        else:
            await message.answer(text=i18n.registration.closed())


    else:
        if await r.exists(str(message.from_user.id)) == 0:
            # User first time in Redis DB - add him to DB      
            new_user_template = {
                'total_games': 0,
                'win': 0,
                'lose': 0,
                'rating': 0,
                'current_game': 0,
                'last_message': 0,
                'wallet': user[0],
                'mnemonics': user[1]
                }
                
            await r.hmset(str(message.from_user.id), new_user_template)
        
        logger.info(f'{message.from_user.id} is old user')
        await dialog_manager.start(state=StartSG.start,
                                   mode=StartMode.RESET_STACK,
                                   data={'user_id': message.from_user.id}
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
