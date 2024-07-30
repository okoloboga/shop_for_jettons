import asyncio
import logging

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter, CommandStart
from redis import asyncio as aioredis
from fluentogram import TranslatorRunner

from ..keyboards import game_process_kb, play_account_kb, enemy_leaved_ok, back_kb
from services import turn_result, game_result
from states import FSMMain

router_game_process = Router()


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Room owner confirmed game
@router_game_process.callback_query(F.data == 'game_confirm', 
                                    StateFilter(FSMMain.wait_game)
                                    )
async def process_game_confirm_button(callback: CallbackQuery, 
                                      state: FSMContext, 
                                      bot: Bot, 
                                      i18n: TranslatorRunner
                                      ):
    logger.info(f'User {callback.from_user.id} confirmed new Game!')
    
    await asyncio.sleep(2)
    r = aioredis.Redis(host='localhost', port=6379)

    # Removing keyboard of last message
    id = callback.message.message_id - 1
    chat_id = callback.chat_instance
    user = await r.hgetall(str(callback.from_user.id))
    user[b'last_message'] = callback.message.message_id
    await r.hmset(str(callback.from_user.id), user)

    try:
        await callback.message.edit_text(text=i18n.rules(),
                                         reply_markup=game_process_kb(i18n))
        await bot.delete_message(chat_id, id)
        
    except TelegramBadRequest:
        await callback.answer()

    await state.set_state(FSMMain.in_game)


"""MAIN GAME PROCESS IN ONE HANDLER"""


@router_game_process.callback_query(F.data.in_(['rock', 'paper', 'scissors']), 
                                    StateFilter(FSMMain.in_game)
                                    )
async def process_game_button(callback: CallbackQuery, 
                              bot: Bot, 
                              state: FSMContext, 
                              i18n: TranslatorRunner
                              ):

    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    user = await r.hgetall(str(callback.from_user.id))
    id = callback.message.message_id - 1
    chat_id = callback.chat_instance
    room_id = int(str(user[b'current_game'], encoding='utf-8'))
    _game = await r.hgetall('g_'+str(room_id))

    logger.info(f"Before writing move: P1 {_game[b'player1_move']}; P2 {_game[b'player2_move']}")

    user[b'last_message'] = callback.message.message_id
    i_am = None
    enemy_am = None
    if int(str(_game[b'player1'], encoding='utf-8')) == callback.from_user.id:
        i_am = b'player1'
        enemy_am = b'player2'
    elif int(str(_game[b'player2'], encoding='utf-8')) == callback.from_user.id:
        i_am = b'player2'
        enemy_am = b'player1'
    move = i_am + b'_move'
    logger.info(f'Move is {move}')

    enemy_id = str(_game[enemy_am], encoding='utf-8')
    enemy = await r.hgetall(enemy_id)

    # Setting players move
    _game[move] = callback.data
    await r.hmset('g_' + str(room_id), _game)
    game = await r.hgetall('g_' + str(room_id))

    # Timing for writing
    await asyncio.sleep(2)
    logger.info(f"After writing move: P1 {game[b'player1_move']}; P2 {game[b'player2_move']}")
    
    # If both players made move
    if game[b'player1_move'] != b'0' and game[b'player2_move'] != b'0':
        
        # Checking result of turn, losers health decreasing
        result = await turn_result(game[b'player1_move'], game[b'player2_move'], room_id, i_am)
        
        # If health of both players is not zero
        if result == 'you_caused_damage':
            try:
                # Return result of turn and keyboard for next move
                await callback.message.edit_text(text=i18n.enemy.damaged(),
                                                 reply_markup=game_process_kb(i18n))
                await bot.delete_message(chat_id, id)
            except TelegramBadRequest:
                await callback.answer()
            # Return to opponent result of turn and keyboard for next move
            await asyncio.sleep(2)
            msg = await bot.send_message(enemy_id, text=i18n.you.damaged(),
                                         reply_markup=game_process_kb(i18n))
            try:
                await bot.delete_message(enemy_id, msg.message_id - 1)
            
            except TelegramBadRequest:
                await bot.delete_message(enemy_id, msg.message_id)
            game[enemy_am + b'_health'] = int(str(game[enemy_am + b'_health'], encoding='utf-8')) - 1
        
        elif result == 'enemy_caused_damaged':
            try:
                # Return result of turn and keyboard for next move
                await callback.message.edit_text(text=i18n.you.damaged(),
                                                 reply_markup=game_process_kb(i18n))
                await bot.delete_message(chat_id, id)
            except TelegramBadRequest:
                await callback.answer()
            # Return to opponent result of turn and keyboard for next move
            await asyncio.sleep(2)
            msg = await bot.send_message(enemy_id, text=i18n.enemy.damaged(),
                                         reply_markup=game_process_kb(i18n))
            try:
                await bot.delete_message(enemy_id, msg.message_id - 1)

            except TelegramBadRequest:
                await bot.delete_message(enemy_id, msg.message_id)
            game[i_am + b'_health'] = int(str(game[i_am + b'_health'], encoding='utf-8')) - 1

        elif result == 'nobody_won':
            try:
                # Return result of turn and keyboard for next move
                await callback.message.edit_text(text=i18n.nobody.won(),
                                                 reply_markup=game_process_kb(i18n))
                await bot.delete_message(chat_id, id)
            except TelegramBadRequest:
                await callback.answer()
            msg = await bot.send_message(enemy_id, text=i18n.nobody.won(),
                                         reply_markup=game_process_kb(i18n))
            try:
                await bot.delete_message(enemy_id, msg.message_id - 1)
            except TelegramBadRequest:
                await bot.delete_message(enemy_id, msg.message_id)
        game[b'player1_move'] = b'0'
        game[b'player2_move'] = b'0'
        await r.hmset(enemy_id, enemy)
        await r.hmset('g_'+str(room_id), game)

        # Checking player1 health for zero
        if game[b'player1_health'] == b'0' or game[b'player1_health'] == 0:
            if i_am == b'player1':
                total_result = 'lose'
                try:
                    # Return result and return to main menu
                    await callback.message.edit_text(text=i18n.lose(),
                                                     reply_markup=back_kb(i18n))
                    await bot.delete_message(chat_id, id)
                except TelegramBadRequest:
                    await callback.answer()
                # Return result to opponent and return to main menu
                await asyncio.sleep(2)
                msg = await bot.send_message(enemy_id, text=i18n.win(),
                                             reply_markup=back_kb(i18n))
                # await bot.delete_message(enemy_id, msg.message_id - 1)
                # Counting total wins, loses, games, jettons
                await game_result(total_result, str(callback.from_user.id), enemy_id, room_id, msg.message_id)
                # Delete game process data
                await r.delete('g_'+str(room_id))
            
            else:
                total_result = 'win'
                try:
                    # Return result and return to main menu
                    await callback.message.edit_text(text=i18n.win(),
                                                     reply_markup=back_kb(i18n))
                    await bot.delete_message(chat_id, id)
                except TelegramBadRequest:
                    await callback.answer()
                # Return result to opponent and return to main menu
                await asyncio.sleep(2)
                msg = await bot.send_message(enemy_id, text=i18n.lose(),
                                             reply_markup=back_kb(i18n))
                # await bot.delete_message(enemy_id, msg.message_id - 1)
                # Counting total wins, loses, games, jettons
                await game_result(total_result, str(callback.from_user.id), enemy_id, room_id, msg.message_id)
            await state.clear()
                  
        # Checking player2 health for zero
        elif game[b'player2_health'] == b'0' or game[b'player2_health'] == 0:
            if i_am == b'player2':
                total_result = 'lose'
                try:
                    # Return result and return to main menu
                    await callback.message.edit_text(text=i18n.lose(),
                                                     reply_markup=back_kb(i18n))
                    await bot.delete_message(chat_id, id)
                except TelegramBadRequest:
                    await callback.answer()
                # Return result to opponent and return to main menu
                await asyncio.sleep(2)
                msg = await bot.send_message(enemy_id, text=i18n.win(),
                                             reply_markup=back_kb(i18n))
                # await bot.delete_message(enemy_id, msg.message_id - 1)
                # Counting total wins, loses, games, jettons
                await game_result(total_result, str(callback.from_user.id), enemy_id, room_id, msg.message_id)

            else:
                total_result = 'win'
                try:
                    # Return result and return to main menu
                    await callback.message.edit_text(text=i18n.win(),
                                                     reply_markup=back_kb(i18n))
                    await bot.delete_message(chat_id, id)
                except TelegramBadRequest:
                    await callback.answer()
                # Return result to opponent and return to main menu
                await asyncio.sleep(2)
                msg = await bot.send_message(enemy_id, text=i18n.lose(),
                                             reply_markup=back_kb(i18n))
                # await bot.delete_message(enemy_id, msg.message_id - 1)
                # Counting total wins, loses, games, jettons
                await game_result(total_result, str(callback.from_user.id), enemy_id, room_id, msg.message_id)
            await state.clear()
    else:
        # Suggest you wait
        try:
            await callback.message.edit_text(text=i18n.choice.made())
            await bot.delete_message(chat_id, id)
        except TelegramBadRequest:
            await callback.answer()


# Canceling game before by Player
@router_game_process.callback_query(F.data == 'end_game', 
                                    StateFilter(FSMMain.in_game)
                                    )
async def process_end_game_button(callback: CallbackQuery, 
                                  bot: Bot, 
                                  state: FSMContext, 
                                  i18n: TranslatorRunner
                                  ):
    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    user = await r.hgetall(str(callback.from_user.id))
    room_id = int(str(user[b'current_game'], encoding='utf-8'))
    game = await r.hgetall('g_' + str(room_id))
    enemy_am = None
    if int(str(game[b'player1'], encoding='utf-8')) == callback.from_user.id:
        enemy_am = b'player2'
    elif int(str(game[b'player1'], encoding='utf-8')) == callback.from_user.id:
        enemy_am = b'player1'
    enemy_id = str(game[enemy_am], encoding='utf-8')
    enemy = await r.hgetall(enemy_id)
    enemy_last_msg = int(str(enemy[b'last_message'], encoding='utf-8'))

    try:
        await callback.message.edit_text(text=i18n.you.leaved(),
                                         reply_markup=play_account_kb(i18n))
        msg = await bot.send_message(enemy_id, text=i18n.enemy.leaved(),
                                     reply_markup=enemy_leaved_ok(i18n))
        await bot.delete_message(enemy_id, enemy_last_msg)
        await state.clear()
        await r.hmset(str(callback.from_user.id), user)
        await game_result('lose', str(callback.from_user.id), enemy_id, room_id, msg.message_id)
    except TelegramBadRequest:
        await callback.answer()

    await r.delete('g_' + str(room_id))


@router_game_process.message(CommandStart(), 
                             StateFilter(FSMMain.in_game)
                             )
async def process_end_game_button_2(message: Message, 
                                    bot: Bot, 
                                    state: FSMContext, 
                                    i18n: TranslatorRunner
                                    ):
    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    user = await r.hgetall(str(message.from_user.id))
    room_id = int(str(user[b'current_game'], encoding='utf-8'))
    game = await r.hgetall('g_' + str(room_id))
    enemy_am = None
    if int(str(game[b'player1'], encoding='utf-8')) == message.from_user.id:
        enemy_am = b'player2'
    elif int(str(game[b'player1'], encoding='utf-8')) == message.from_user.id:
        enemy_am = b'player1'
    enemy_id = str(game[enemy_am], encoding='utf-8')
    enemy = await r.hgetall(enemy_id)
    enemy_last_msg = int(str(enemy[b'last_message'], encoding='utf-8'))

    await message.edit_text(text=i18n.you.leaved(),
                            reply_markup=play_account_kb(i18n))
    msg = await bot.send_message(enemy_id, text=i18n.enemy.leaved(),
                                 reply_markup=enemy_leaved_ok(i18n))
    await bot.delete_message(enemy_id, enemy_last_msg)
    await state.clear()
    await r.hmset(str(message.from_user.id), user)
    await game_result('lose', str(message.from_user.id), enemy_id, room_id, msg.message_id)

    await r.delete('g_' + str(room_id))
