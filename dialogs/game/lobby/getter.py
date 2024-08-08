import logging

from aiogram import Bot
from aiogram_dialog import DialogManager
from aiogram.types import User
from aiogram.utils.deep_linking import create_start_link
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncEngine
from redis import asyncio as aioredis

from services import get_user_account_data, jetton_value, ton_value


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Main lobby Getter
async def lobby_menu_getter(dialog_manager: DialogManager,
                            db_engine: AsyncEngine,
                            i18n: TranslatorRunner,
                            event_from_user: User,
                            **kwargs) -> dict:
    
    user_id = event_from_user.id
    logger.info(f'User {user_id} in lobby_menu_getter')
    costumers_dict = await get_user_account_data(user_id,
                                                 db_engine)
    wallet = costumers_dict['address']    
    
    # Write jettons and TON value to dialog data
    dialog_manager.current_context().dialog_data['jettons'] = await jetton_value(wallet)
    dialog_manager.current_context().dialog_data['ton'] = await ton_value(wallet)
    dialog_manager.current_context().dialog_data['wallet'] = wallet     

    return {'lobby_menu': i18n.chose.action(),
            'button_play': i18n.play(),
            'button_stats': i18n.stats(),
            'button_back': i18n.button.back()}


# Select - Create or Join to Game
async def create_join_getter(dialog_manager: DialogManager,
                             db_engine: AsyncEngine,
                             i18n: TranslatorRunner,
                             event_from_user: User,
                             **kwargs) -> dict:
    
    user_id = event_from_user.id
    logger.info(f'User {user_id} in create_join_getter')

    return {'create_join': i18n.ready(),
            'button_create_game': i18n.create.button(),
            'button_join_game': i18n.join.button(),
            'button_back': i18n.button.back()}


# Select Bet
async def make_bet_getter(dialog_manager: DialogManager,
                          db_engine: AsyncEngine,
                          i18n: TranslatorRunner,
                          event_from_user: User,
                          **kwargs) -> dict:
    
    user_id = event_from_user.id
    logger.info(f'User {user_id} in select Bet')

    return {'make_bet': i18n.bet(),
            'button_bet_1': i18n.b1(),
            'button_bet_2': i18n.b2(),
            'button_bet_3': i18n.b3(),
            'button_bet_4': i18n.b4(),
            'button_bet_5': i18n.b5(),
            'button_bet_25': i18n.b25(),
            'button_back': i18n.button.back()}


# Show all avaliable games
async def search_game_getter(dialog_manager: DialogManager,
                             db_engine: AsyncEngine,
                             i18n: TranslatorRunner,
                             event_from_user: User,
                             **kwargs) -> dict:
   
    r = aioredis.Redis(host='localhost', port=6379)
    rooms_list = []
    
    for key in await r.keys("r_*"):
        logger.info(f'key of r.keys("r_*) is {key}')
        rooms_list.append((int(str(key, encoding='utf-8')[2:]), int(str(await r.get(key), encoding='utf-8'))))

    logger.info(f'Total rooms list: {rooms_list}')

    return {'search_game': i18n.search.game(), 
            'rooms_list': rooms_list,
            'button_back': i18n.button.back()}
                     

# Waiting for Game as Creator
async def waiting_game_getter(dialog_manager: DialogManager,
                              db_engine: AsyncEngine,
                              i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs) -> dict:
    
    user_id = event_from_user.id
    logger.info(f'User {user_id} in waiting_game_getter')

    return {'waiting_game': i18n.yes.wait(),
            'button_wait': i18n.button.wait(),
            'button_back': i18n.button.back()}


# Game is founded - lets join!
async def game_confirm_getter(dialog_manager: DialogManager,
                              db_engine: AsyncEngine,
       i18n: TranslatorRunner,
                              event_from_user: User,
                              **kwargs) -> dict:
    
    user_id = event_from_user.id
    logger.info(f"User: {user_id} confirming game")
    game = dialog_manager.current_context().dialog_data['game']

    # If User is Game Owner
    if int(user_id) == int(game):
        r = aioredis.Redis(host='localhost', port=6379)
        game_data = await r.hgetall('g_'+str(game))
        game_data[b'owner_ready'] = 1
        await r.hmset('g_'+str(game), game_data)
        logger.info(f'Game Owner of {game_data} is ready!')

    return {'game_confirm': i18n.game.confirm(),
            'button_game_confirm': i18n.button.game.confirm()}
