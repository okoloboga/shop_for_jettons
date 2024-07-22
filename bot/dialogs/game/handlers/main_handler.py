import logging
import pprint

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner
from redis import asyncio as aioredis

from ..keyboards import create_join_kb, play_account_kb, back_kb
from states import StartSG
from config import get_config, BotConfig

router_game_menu = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# START command
@router_game_menu.callback_query(StateFilter(StartSG.start))
async def process_start_command(callback: CallbackQuery,
                                button: Button,
                                dialog_manager: DialogManager
                                ):
    logger.info(f'User {callback.from_user.id} enter the Game')

    await dialog_manager.reset_stack()
     
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        
    msg = await callback.message.answer(text=i18n.chose.action(),
                                        reply_markup=play_account_kb(i18n))
    # Init Bot
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    await bot.delete_message(callback.from_user.id, msg.message_id - 1)
    
    logger.info(f'Last message {msg.message_id - 1} is deleted')
    

# Canceling anything in states
@router_game_menu.callback_query(F.data == 'back', ~StateFilter(default_state))
async def process_back_waiting_button(callback: CallbackQuery, 
                                      state: FSMContext, 
                                      i18n: TranslatorRunner
                                      ):
    
    r = aioredis.Redis(host='localhost', port=6379)

    try:
        logger.info(f'User {callback.from_user.id} pressed BACK in Game Menu')
        
        await callback.message.edit_text(text=i18n.start(),
                                         reply_markup=play_account_kb(i18n))
        
        user = await r.hgetall(str(callback.from_user.id))
        logger.info(f'Users {callback.from_user.id} data: {pprint.pprint(user)}')
        
        user[b'current_game'] = 0
        await r.hmset(str(callback.from_user.id), user)
        
        if await r.exists("r_" + str(callback.from_user.id)) != 0:
            await r.delete("r_" + str(callback.from_user.id))
            
    except TelegramBadRequest:
        await callback.answer()
        
    await state.clear()


# PLAY button pressing
@router_game_menu.callback_query(F.data == 'play', 
                                 StateFilter(default_state)
                                 )
async def process_play_button(callback: CallbackQuery, 
                              state: FSMContext, 
                              i18n: TranslatorRunner
                              ):
    
    logger.info(f'User {callback.from_user.id} pressed Play in Game Menu')
    
    try:
        await callback.message.edit_text(text=i18n.ready(),
                                         reply_markup=create_join_kb(i18n))
        await state.clear()
        
    except TelegramBadRequest:
        await callback.answer()


# STATS button pressing
@router_game_menu.callback_query(F.data == 'stats', 
                                 StateFilter(default_state)
                                 )
async def process_stats_button(callback: CallbackQuery, 
                               state: FSMContext, 
                               i18n: TranslatorRunner
                               ):
    
    logger.info(f'User {callback.from_user.id} pressed Stats in Game Menu')
    
    r = aioredis.Redis(host='localhost', port=6379)

    try:
        user = await r.hgetall(str(callback.from_user.id))
        logger.info(f'Users {callback.from_user.id} data: {user}')
        
        await callback.message.edit_text(
            text=i18n.statistic(total_games=str(user[b'total_games'], encoding='utf-8'),
                                win=str(user[b'win'], encoding='utf-8'),
                                lose=str(user[b'lose'], encoding='utf-8'),
                                rating=str(user[b'rating'], encoding='utf-8'),
                                ),
            reply_markup=back_kb(i18n))
        
    except TelegramBadRequest:
        await callback.answer()


# BACK button pressing without states
@router_game_menu.callback_query(F.data == 'back', 
                                 StateFilter(default_state)
                                 )
async def process_back_button(callback: CallbackQuery, 
                              i18n: TranslatorRunner
                              ):
    
    logger.info(f'User {callback.from_user.id} pressed Back in Game Menu without states')
    
    try:
        await callback.message.edit_text(text=i18n.start(id=callback.from_user.id),
                                         reply_markup=play_account_kb(i18n))
    except TelegramBadRequest:
        await callback.answer()
        

# TOTAL BACK button pressing - go to the start menu of Bot
@router_game_menu.callback_query(F.data == 'total_back',
                                 StateFilter(default_state)
                                 )
async def process_total_back_button(callback: CallbackQuery,
                                    i18n: TranslatorRunner,
                                    dialog_manager: DialogManager
                                    ):
    
    logger.info(f'User {callback.from_user.id} pressed Total Back in Game Menu')
    await dialog_manager.start(state=StartSG.start,
                               data={'user_id': callback.from_user.id}
                               )
    