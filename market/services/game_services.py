import asyncio
import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest
from aiogram_dialog import DialogManager, StartMode
from fluentogram import TranslatorRunner
from redis import asyncio as aioredis
from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database import stats
from config import get_config, WalletConfig
from states import LobbySG
from .admin_services import get_user_data
from dialogs.game.game import game_end

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

r = aioredis.Redis(host='redis', port=6379, db=0)


# Get User stats from database
async def get_user_stats(db_engine: AsyncEngine,
                         user_id: int) -> dict:

    stats_stmt = (
        select("*")
        .select_from(stats)
        .where(stats.c.telegram_id == user_id)
    )

    async with db_engine.connect() as conn:
        stats_data_raw = await conn.execute(stats_stmt)
        for row in stats_data_raw:
            user_stats = list(row)

    return {"telegram_id": user_stats[0],
            "total_games": user_stats[1],
            "wins": user_stats[2],
            "loses": user_stats[3],
            "rate": user_stats[4]}


# Returns key of dict by users answer as value
def normalize_answer(i18n: TranslatorRunner, 
                     user_answer: str
                     ) -> str:
    
    game = {'rock': i18n.rock(),
            'paper': i18n.paper(),
            'scissors': i18n.scissors()}
    for key in game:
        if game[key] == user_answer:
            break
    return key


# Redirection of turn result
async def turn_result(player1_move: str | bytes, 
                      player2_move: str | bytes, 
                      player1_health: str | bytes,
                      player2_health: str | bytes,
                      room_id: str | int, 
                      i_am: str | bytes
                      ) -> str:
    
    # Get winner
    rules = {b'rock': b'scissors',
             b'scissors': b'paper',
             b'paper': b'rock'}
    result: str  # Result of turn 


    if player1_move == player2_move:
        result = 'nobody_won'
    elif rules[player1_move] == Splayer2_move:
        if int(str(player2_health, encoding='utf-8')) > 0:
            result = b'player2_damaged'
        else:
            result = b'player1_won'
    else:
        if int(str(player1_health, encoding='utf-8')) > 0:
            result = b'player1_damaged'
        else:
            result = b'player2_won'

    if result == 'nobody_won':
        return 'nobody_won'
    elif result == b'player1_damaged':
        if result[:7] == i_am:
            return 'enemy_caused_damaged'
        else:
            return 'you_caused_damage'
    elif result == b'player2_damaged':
        if result[:7] == i_am:
            return 'enemy_caused_damaged'
        else:
            return 'you_caused_damage'
    elif result == b'player1_won':
        if result[:7] == i_am:
            return 'you_win'
        else:
            return 'you_lose'
    elif result == b'player2_won':
        if result[:7] == i_am:
            return 'you_win'
        else:
            return 'you_lose'


# Writing data from Game Result to Database
async def write_game_result(db_engine: AsyncEngine,
                            result: dict):
                            
    logger.info(f'Writing data about result of game in database: {result}')

    # Get wallets from Database
    winner_wallet = (await get_user_data(int(result['winner']), 
                                         db_engine))['address']
    loser_private_key = (await get_user_data(int(result['loser']), 
                                             db_engine))['private_key']

    logger.info(f"Winner wallet: {winner_wallet}\nLoser private key: {private_key}")
    
    winner_old_stats = await get_user_stats(db_engine, 
                                             int(result['winner']))
    loser_old_stats = await get_user_stats(db_engine,
                                           int(result['loser']))

    logger.info(f"Winner old stats: {winner_old_stats}\n Loser old stats: {loser_old_stats}")

    winner_stats_stmt = (stats.update()
                         .values(total_games = int(winner_old_stats['total_games']) + 1,
                                 wins = int(winner_old_stats['wins']) + 1,
                                 rate = (int(winner_old_stats['wins']) + 1) / (int(winner_old_stats['total_games']) + 1))
                         .where(stats.c.telegram_id == int(result['winner'])))

    loser_stats_stms = (stats.update()
                        .values(total_games = int(loser_old_stats['total_games']) + 1,
                                loses = int(loser_old_stats['loses']) + 1,
                                rate = int(loser_old_stats['wins']) / (int(loser_old_stats['total_games']) + 1))
                        .where(stats.c.telegram_id == int(result['loser'])))

    async with db_engine.connect() as conn:
        await conn.execute(winner_stats_stmt)
        await conn.execute(loser_stats_stms)
        await conn.commit()
        logger.info(f"New stats writed for winner {result['winner']} and loser {result['loser']}")
    
    central_wallet = get_config(WalletConfig, 'wallet')

    '''
    DISABLED FOR TESTS
    await send_token(owner=central_wallet.centralWallet,
                     private_key=loser_private_key,
                     target=winner_wallet,
                     amount=int(result['bet'])
                     )
    '''
    logger.info(f'Tokens for game transfered')


# Making dict with game results
async def game_result(callback: CallbackQuery,
                      dialog_manager: DialogManager,
                      total_result: str,
                      enemy_id: int,
                      user_id: int,
                      game: dict,
                      i18n: TranslatorRunner,
                      bot: Bot,
                      game_end: InlineKeyboardMarkup):


    logger.info(f"Game result: total_result - {total_result}, enemy_id - {enemy_id}, user_id - {user_id}")
    game_id = str(game[b'player1'], encoding='utf-8')
    task = [task for task in asyncio.all_tasks() if task.get_name() == f'timer_{game_id}']
    print(task)
    task[0].cancel()
    bet = str(game[b'bet'], encoding='utf-8')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')
    message_map = {'loser': i18n.lose(),
                   'winner': i18n.win()}
    result = {'winner': enemy_id if total_result == 'lose' else user_id,
              'loser': enemy_id if total_result == 'win' else user_id,
              'bet': bet}

    # Clear cache of Redis
    await r.delete('g_'+str(game[b'player1'], encoding='utf-8'))
    await r.delete(str(user_id))
    await r.delete(str(enemy_id))
    await r.delete('wait_'+str(user_id))
    await r.delete('wait_'+str(enemy_id))
    await r.delete('result_'+str(user_id))
    await r.delete('result_'+str(enemy_id))

    # Writing Game results to Database
    await write_game_result(db_engine, result)

    user_msg = await bot.send_message(user_id, 
                                      text=message_map[
                                          'winner' if result['winner'] == user_id else 'loser'
                                          ])
    try:
        await bot.delete_messages(user_id, [msg for msg in range(user_msg.message_id-1, user_msg.message_id - 10, -1)])
    except TelegramBadRequest as ex:
                   logger.info(f'{ex.message}')

    await dialog_manager.start(state=LobbySG.main,
                               mode=StartMode.RESET_STACK,
                               data={**result})

    # Return result to opponent and return to main menu
    enemy_msg = await bot.send_message(enemy_id, 
                                       text=message_map[
                                           'winner' if result['winner'] == enemy_id else 'loser'
                                           ],
                                       reply_markup=game_end(i18n))
    try: 
        await bot.delete_messages(enemy_id, [msg for msg in range(enemy_msg.message_id-1, enemy_msg.message_id - 10, -1)])
    except TelegramBadRequest as ex:
        logger.info(f'{ex.message}')


# Timing starts
async def timer(dialog_manager: DialogManager, 
                room_id: int):

    await asyncio.sleep(120)
    game = await r.hgetall('g_' + str(room_id))
    if len(game) == 0:
        logger.info(f"g_{room_id} doesn't exist")
        await dialog_manager
        pass
    else:
        game = await r.hgetall('g_' + str(room_id))
        player1 = str(game[b'player1'], encoding='utf-8')
        player2 = str(game[b'player2'], encoding='utf-8')
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        bot: Bot = dialog_manager.middleware_data.get('bot')

        # Nobody made move
        if game[b'player1_move'] == game[b'player2_move'] == b'0':
            
            # Writig result to database, clearing Redis cache
            await r.delete(str(player1))
            await r.delete(str(player2))
            await r.delete('g_'+str(game[b'player1'], encoding='utf-8'))
            await r.delete('wait_'+str(player1))
            await r.delete('wait_'+str(player2))
            await r.delete('result_'+str(player1))
            await r.delete('result_'+str(player2))

            # Send Notifivations to players
            player1_msg = await bot.send_message(player1, 
                                                 text=i18n.time.end(),
                                                 reply_markup=game_end(i18n))
            try:
                await bot.delete_messages(player1, 
                                          [msg for msg in range(player1_msg.message_id-1, player1_msg.message_id - 10, -1)])
            except TelegramBadRequest as ex:
                logger.info(f'{ex.message}')
            
            player2_msg = await bot.send_message(player2, 
                                                 text=i18n.time.end(),
                                                 reply_markup=game_end(i18n))
            try: 
                await bot.delete_messages(player2, 
                                          [msg for msg in range(player2_msg.message_id-1, player2_msg.message_id - 10, -1)])
            except TelegramBadRequest as ex:
                logger.info(f'{ex.message}')

        else:
            result: dict  # Init dict to write results of game
            # Player1 win
            if game[b'player1_move'] != b'0':
                
                # Writing data to Database and clearing Redis cache
                result = {'winner':  player1,
                          'loser': player2,
                          'bet': int(str(game[b'bet'], encoding='utf-8'))}
                 
            # Player2 win
            elif game[b'player2_move'] != b'0':
                result = {'winner':  player2,
                          'loser': player1,
                          'bet': int(str(game[b'bet'], encoding='utf-8'))}
            
            # Writig result to database, clearing Redis cache
            db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')
            await write_game_result(db_engine, result)
            await r.delete(str(player1))
            await r.delete(str(player2))
            await r.delete('g_'+str(game[b'player1'], encoding='utf-8'))
            await r.delete('wait_'+str(player1))
            await r.delete('wait_'+str(player2))
            await r.delete('result_'+str(player1))
            await r.delete('result_'+str(player2))
            
            message_map = {'loser': i18n.lose(),
                           'winner': i18n.win()}

            logger.info(f"Winner: {result['winner']}; Loser: {result['loser']}")
            logger.info(f'Player1: {player1}; Player2 {player2}')
            
            # Send Notifivations to players
            winner_msg = await bot.send_message(player1, 
                                                text=message_map[
                                                  'winner' if int(result['winner']) == int(player1) else 'loser'
                                                  ],
                                                reply_markup=game_end(i18n))
            try:
                await bot.delete_messages(player1, 
                                          [msg for msg in range(winner_msg.message_id-1, winner_msg.message_id - 10, -1)])
            except TelegramBadRequest as ex:
                logger.info(f'{ex.message}')
            
            loser_msg = await bot.send_message(player2, 
                                               text=message_map[
                                                   'winner' if int(result['winner']) == int(player2) else 'loser'
                                                   ],
                                               reply_markup=game_end(i18n))
            try: 
                await bot.delete_messages(player2, 
                                          [msg for msg in range(loser_msg.message_id-2, loser_msg.message_id - 10, -1)])
            except TelegramBadRequest as ex:
                logger.info(f'{ex.message}')



