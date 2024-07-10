import asyncio
import sys
sys.path.append("..")

from aiogram import Bot
from fluentogram import TranslatorRunner
from redis import asyncio as aioredis

r = aioredis.Redis(host='localhost', port=6379)


# Returns key of dict by users answer as value
def normalize_answer(i18n: TranslatorRunner, user_answer: str) -> str:
    game = {'rock': i18n.rock(),
            'paper': i18n.paper(),
            'scissors': i18n.scissors()}
    for key in game:
        if game[key] == user_answer:
            break
    return key


# Define winner of turn
async def _get_winner(player1_move: str | bytes, player2_move: str | bytes, room_id: str | int) -> str:
    game = await r.hgetall('g_'+str(room_id))
    rules = {b'rock': b'scissors',
             b'scissors': b'paper',
             b'paper': b'rock'}
    if player1_move == player2_move:
        return 'nobody_won'
    elif rules[player1_move] == player2_move:
        if int(str(game[b'player2_health'], encoding='utf-8')) > 0:
            return b'player2_damaged'
        else:
            return b'player1_won'
    else:
        if int(str(game[b'player1_health'], encoding='utf-8')) > 0:
            return b'player1_damaged'
        else:
            return b'player2_won'


# Redirection of turn result
async def turn_result(player1_move: str | bytes, player2_move: str | bytes, room_id: str | int, i_am: str | bytes) -> str:
    result = await _get_winner(player1_move, player2_move, room_id)
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


# Changing account stats after game
async def game_result(result: str, my_id: str, enemy_id: str, room_id: str | int, msg_id: int):
    user = await r.hgetall(my_id)
    enemy = await r.hgetall(enemy_id)
    game = await r.hgetall('g_'+str(room_id))

    if result == 'lose':
        # Player lose
        user[b'total_games'] = int(str(user[b'total_games'], encoding='utf-8')) + 1
        user[b'lose'] = int(str(user[b'lose'], encoding='utf-8')) + 1
        user[b'rating'] = int(int(str(user[b'win'], encoding='utf-8')) / user[b'total_games'] * 1000)
        user[b'current_game'] = b'0'
        enemy[b'total_games'] = int(str(enemy[b'total_games'], encoding='utf-8')) + 1
        enemy[b'win'] = int(str(enemy[b'win'], encoding='utf-8')) + 1
        enemy[b'rating'] = int(enemy[b'win'] / enemy[b'total_games'] * 1000)
        enemy[b'current_game'] = b'0'
        enemy[b'last_message'] = msg_id

    else:
        # Player wins
        user[b'total_games'] = int(str(user[b'total_games'], encoding='utf-8')) + 1
        user[b'win'] = int(str(user[b'win'], encoding='utf-8')) + 1
        user[b'rating'] = int(user[b'win'] / user[b'total_games'] * 1000)
        user[b'current_game'] = b'0'
        enemy[b'total_games'] = int(str(enemy[b'total_games'], encoding='utf-8')) + 1
        enemy[b'lose'] = int(str(enemy[b'lose'], encoding='utf-8')) + 1
        enemy[b'rating'] = int(int(str(enemy[b'win'], encoding='utf-8')) / enemy[b'total_games'] * 1000)
        enemy[b'current_game'] = b'0'
        enemy[b'last_message'] = msg_id

    await r.hmset(my_id, user)
    await r.hmset(enemy_id, enemy)
    await r.delete('g_' + str(room_id))


# Timing starts
async def timer(bot: Bot, 
                i18n: TranslatorRunner, 
                room_id: int,
                play_account_kb):
    await asyncio.sleep(120)
    if await r.exists('g_' + str(room_id)) == 0:
        pass
    else:
        game = await r.hgetall('g_' + str(room_id))
        player1_id = str(game[b'player1'], encoding='utf-8')
        player2_id = str(game[b'player2'], encoding='utf-8')
        player1 = await r.hgetall(player1_id)
        player2 = await r.hgetall(player2_id)
        msg1 = int(str(player1[b'last_message'], encoding='utf-8'))
        msg2 = int(str(player2[b'last_message'], encoding='utf-8'))
        print(msg1)
        print(msg2)

        # Nobody made move
        if game[b'player1_move'] == game[b'player2_move'] == b'0':
            # Nobody won
            await r.delete('r_' + str(room_id))
            await bot.delete_message(player1_id, msg1)
            await bot.delete_message(player2_id, msg2)
            await bot.send_message(chat_id=player1_id,
                                   text=i18n.chose.action(),
                                   reply_markup=play_account_kb(i18n))
            await bot.send_message(chat_id=player2_id,
                                   text=i18n.chose.action(),
                                   reply_markup=play_account_kb(i18n))
        # Player1 win
        elif game[b'player1_move'] != b'0':
            await game_result('win', player1_id, player2_id, room_id, msg2)
            await bot.delete_message(player1_id, msg1)
            await bot.delete_message(player2_id, msg2)
            await bot.send_message(player1_id, text=i18n.win(),
                                   reply_markup=play_account_kb(i18n))
            await bot.send_message(player2_id, text=i18n.lose(),
                                   reply_markup=play_account_kb(i18n))
        # Player2 win
        elif game[b'player2_move'] != b'0':
            await game_result('win', player2_id, player1_id, room_id, msg1)
            await bot.delete_message(player1_id, msg1)
            await bot.delete_message(player2_id, msg2)
            await bot.send_message(player2_id, text=i18n.win(),
                                   reply_markup=play_account_kb(i18n))
            await bot.send_message(player1_id, text=i18n.lose(),
                                   reply_markup=play_account_kb(i18n))
