import logging
import asyncio
import services.game_services

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncEngine
from redis import asyncio as aioredis

from states import LobbySG, StartSG


router_lobby = Router()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(filename)s:%(lineno)d #%(levelname)-8s '
                           '[%(asctime)s] - %(name)s - %(message)s')


# Process lobby_play button
async def lobby_play(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):
    
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed lobby_play")
    
    dialog_manager.current_context().dialog_data['game'] = None

    await dialog_manager.switch_to(LobbySG.create_join)


# Process lobby_create button
async def lobby_create(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager):

    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed lobby_create")
    
    if dialog_manager.current_context().dialog_data['game'] is None:
        await dialog_manager.switch_to(LobbySG.make_bet)

    else:
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        await callback.message.answer(text=i18n.already.ingame())


# Process lobby_join button
async def lobby_join(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed lobby_join")

    r = aioredis.Redis(host='localhost', port=6379)
    rooms = {}
    
    for key in await r.keys("r_*"):
        logger.info(f'key of r.keys("r_*) is {key}')
        rooms.update({str(key, encoding='utf-8'): str(await r.get(key), encoding='utf-8')})

    # Checking for existing games of this player
    if dialog_manager.current_context().dialog_data['game'] is not None:
        
        logger.info(f'User {user_id} already in game')
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')           
        await callback.message.answer(text=i18n.already.ingame())
    else:

        # If no games        
        if len(rooms) == 0:
            logger.info(f'User {user_id} found no Games, offer to become first')
            i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
            await callback.message.answer(text=i18n.you.first())
            await dialog_manager.switch_to(LobbySG.create_join)
        else:
            logger.info(f'User {user_id} go to select enemy, rooms {rooms}')
            await dialog_manager.switch_to(LobbySG.select_enemy)


# Process lobby_stats button
async def lobby_stats(callback: CallbackQuery,
                      button: Button,
                      dialog_manager: DialogManager):

    get_user_stats = services.game_services.get_user_stats
    user_id = callback.from_user.id
    logger.info(f"Getting stats of User {user_id}")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    user_stats = await get_user_stats(db_engine, user_id)    
    await callback.message.answer(text=i18n.statistic(total_games=user_stats['total_games'],
                                                      win=user_stats['wins'],
                                                      lose=user_stats['loses'],
                                                      rating=user_stats['rate']))


# Making Bet - need to get bet from callback.data
async def bet(callback: CallbackQuery,
              button: Button,
              dialog_manager: DialogManager):

    bet = str(callback.data)[6:]
    user_id = callback.from_user.id
    jettons = dialog_manager.current_context().dialog_data['jettons']
    ton = dialog_manager.current_context().dialog_data['ton']
    wallet = dialog_manager.current_context().dialog_data['wallet']
    logger.info(f"User {user_id} made bet {bet}")

    # Get wallet balance of user

    # If player have not enough jettons
    if int(bet) > int(jettons):
        logger.info(f'User {user_id} have not enough jettons')
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')    
        await callback.message.answer(text=i18n.notenough())

    elif float(ton) < 0.065:
        logger.info(f'User {user_id} have not enough TON')
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        await callback.message.answer(text=i18n.notenough.ton(wallet=wallet))
    else:
        # Creating new room
        r = aioredis.Redis(host='localhost', port=6379)
        await r.set('r_'+str(user_id), bet)
       
        logger.info(f'User {user_id} created new room with bet {bet}')
     
        # Setting flag of waiting for game
        dialog_manager.current_context().dialog_data['game'] = user_id
        await dialog_manager.switch_to(LobbySG.wait_game)


# Process Wait button - refresh game search
async def wait_game(callback: CallbackQuery,
                    button: Button,
                    dialog_manager: DialogManager):

    user_id = callback.from_user.id
    logger.info(f"User {user_id} still waiting for game...")

    r = aioredis.Redis(host='localhost', port=6379)

    # Checking for update of game start
    if await r.exists('g_'+str(user_id)) != 0:
            
        logger.info(f'User {user_id} ready in his own Game!')
        await dialog_manager.switch_to(LobbySG.game_confirm)

    else:
        
        logger.info(f'User {user_id} still wait for Game')
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')    
        await callback.message.answer(text=i18n.still.wait())


# Process game_selection button - select enemy for game
async def game_selection(callback: CallbackQuery,
                         widget: Select,
                         dialog_manager: DialogManager,
                         selected_game_raw: str):

    selected_game = (selected_game_raw[1:-1]).split(', ')
    user_id = callback.from_user.id
    logger.info(f"User {user_id} select enemy {selected_game}")
    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    bet = int(selected_game[1])
    enemy_id = int(selected_game[0])
    dialog_manager.current_context().dialog_data['bet'] = bet
    user_jettons = dialog_manager.current_context().dialog_data['jettons']
    user_ton = dialog_manager.current_context().dialog_data['ton']
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    logger.info(f'Vars initializated:\n{user_id} VS {enemy_id}; Bet:')

    # Player select himself
    if int(user_id) == int(enemy_id):
        logger.info(f'User {user_id} selected himseff =(')
        await callback.message.answer(text=i18n.selfgame())

    # Chosen game ended or started with another player already
    elif await r.exists('r_'+str(enemy_id)) is None:
        logger.info(f'User {user_id} selected unexisting Game =(')
        await callback.message.answer(text=i18n.no.game())

    # Player have not enough jettons to make current bet
    elif int(bet) > int(user_jettons):
        logger.info(f'User {user_id} have not enought jettons for Bet')
        await callback.message.answer(text=i18n.notenough())

    # Player have not enough TON to pay fee
    elif float(user_ton) < 0.001:
        logger.info(f'User {callback.from_user.id} have not enough TON for fee')
        await callback.message.answer(text=i18n.notenough.ton(wallet=user_ton))
    
    # All is great, game starts
    else:
        timer = services.game_services.timer
        logger.info(f'User {user_id} game could be start in room id {enemy_id}')
        logger.info(f"Bet: {selected_game[1]}")

        dialog_manager.current_context().dialog_data['game'] = enemy_id
        game = {'player1': int(enemy_id),
                'player2': int(user_id),
                'bet': int(selected_game[1]),
                'player1_move': 0,
                'player2_move': 0,
                'player1_health': 2,
                'player2_health': 2,
                'owner_ready': 0}
        logger.info(f'Game created {game}')
        
        await r.hmset('g_'+str(enemy_id), game)

        # Deleting waiting/lobby room and start timer
        await r.delete('r_'+str(enemy_id))

        await dialog_manager.switch_to(LobbySG.game_confirm)



# Process Exit from game - from lobby and game
async def back(callback: CallbackQuery,
               button: Button,
               dialog_manager: DialogManager
               ):

    user_id = callback.from_user.id
    r = aioredis.Redis(host='localhost', port=6379)
    if await r.exists('r_'+str(user_id)):
        await r.delete('r_'+str(user_id))
        logger.info(f'room {user_id} - deleted')
                    
    logger.info(f'Process Back command from non-default state by user {callback.from_user.id}')
    await dialog_manager.start(state=StartSG.start,
                               mode=StartMode.RESET_STACK,
                               data={'user_id': callback.from_user.id}
                               )


