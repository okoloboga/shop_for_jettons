import asyncio
import logging
import services.game_services

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from redis import asyncio as aioredis
from fluentogram import TranslatorRunner

from .keyboards import game_process_kb, game_end
from states import GameSG, LobbySG

router_game = Router()


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Room owner confirmed game
@router_game.callback_query(F.data == 'b_game_confirm', 
                            StateFilter(LobbySG.game_confirm)
                            )
async def game_confirm(callback: CallbackQuery, 
                       button: Button,
                       dialog_manager: DialogManager
                       ):
    r = aioredis.Redis(host='localhost', port=6379)

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')
    game = dialog_manager.current_context().dialog_data['game']
    user_id = callback.from_user.id
    logger.info(f'User {user_id} confirmed new Game!')
    game_data = await r.hgetall('g_'+str(game))
    logger.info(f'Game Data is: {game_data}')

    if str(game_data[b'owner_ready'], encoding='utf-8') == '1':
        await dialog_manager.reset_stack()
        await r.set(str(user_id), str(game))
        logger.info(f'Writed game {game} to Users Redis {user_id}')

        await callback.message.answer(text=i18n.rules(),
                                      reply_markup=game_process_kb(i18n))
        await state.set_state(GameSG.main)
    
    elif int(game) != int(user_id):
        await callback.message.answer(text=i18n.owner.notready())
    await asyncio.sleep(1)
    
    if int(user_id) == int(game):
        timer = services.game_services.timer
        await asyncio.create_task(timer(dialog_manager, int(user_id)), name=f'timer_{game}')




"""MAIN GAME PROCESS IN ONE HANDLER"""


@router_game.callback_query(F.data.in_(['rock', 'paper', 'scissors', 'check', 'end_game']), 
                            StateFilter(GameSG.main)
                            )
async def process_game_button(callback: CallbackQuery, 
                              state: FSMContext, 
                              i18n: TranslatorRunner,
                              dialog_manager: DialogManager,
                              bot: Bot
                              ):
    if callback.data == 'end_game':
        await dialog_manager.start(state=LobbySG.main,
                                   mode=StartMode.RESET_STACK)
    else:
        r = aioredis.Redis(host='localhost', port=6379)

        # Vars initialization
        turn_result = services.game_services.turn_result
        game_result = services.game_services.game_result

        user_id = callback.from_user.id
        room_id = str(await r.get(user_id), encoding='utf-8')
        logger.info(f'room_id: {room_id}')
        _game = await r.hgetall('g_'+str(room_id))

        logger.info(f"Before writing move: P1 {_game[b'player1_move']}; P2 {_game[b'player2_move']}")

        if int(str(_game[b'player1'], encoding='utf-8')) == callback.from_user.id:
            i_am = b'player1'
            enemy_am = b'player2'
        elif int(str(_game[b'player2'], encoding='utf-8')) == callback.from_user.id:
            i_am = b'player2'
            enemy_am = b'player1'
        move = i_am + b'_move'

        player1 = int(str(_game[b'player1'], encoding='utf-8'))
        player2 = int(str(_game[b'player2'], encoding='utf-8'))

        enemy_id = player1 if player1 != user_id else player2

        if callback.data != 'check':
            # Setting players move
            _game[move] = callback.data
            await r.hmset('g_' + str(room_id), _game)

        game = await r.hgetall('g_' + str(room_id))

        # Timing for writing
        await asyncio.sleep(1)
        logger.info(f"After writing move: P1 {game[b'player1_move']}; P2 {game[b'player2_move']}")
        logger.info(f"user_id = {user_id}, enemy_id = {enemy_id}")

        # If both players made move
        if game[b'player1_move'] != b'0' and game[b'player2_move'] != b'0':
            
            # Checking result of turn, losers health decreasing
            result = await turn_result(game[b'player1_move'], 
                                       game[b'player2_move'], 
                                       game[b'player1_health'],
                                       game[b'player2_health'],
                                       room_id,
                                       i_am)
            
            # If health of both players is not zero
            if result == 'you_caused_damage':

                # Write result to Redis
                await r.set('result_'+str(user_id), result)

                try:
                    # Return result of turn and keyboard for next move
                    await callback.message.edit_text(text=i18n.enemy.damaged(),
                                                     reply_markup=game_process_kb(i18n))

                except TelegramBadRequest:
                    await callback.answer()
                
                # Return to opponent result of turn and keyboard for next move
                await asyncio.sleep(1)
                msg = await bot.send_message(enemy_id, 
                                             text=i18n.you.damaged(),
                                             reply_markup=game_process_kb(i18n))
                try:
                    await bot.delete_message(enemy_id, msg.message_id - 1)
                
                except TelegramBadRequest:
                    await callback.answer()
                game[enemy_am + b'_health'] = int(str(game[enemy_am + b'_health'], encoding='utf-8')) - 1
            
            elif result == 'enemy_caused_damaged':
     
                # Write result to Redis
                await r.set('result_'+str(user_id), result)

                try:
                    # Return result of turn and keyboard for next move
                    await callback.message.edit_text(text=i18n.you.damaged(),
                                                     reply_markup=game_process_kb(i18n))
                except TelegramBadRequest:
                    await callback.answer()
     
                # Return to opponent result of turn and keyboard for next move
                await asyncio.sleep(1)
                msg = await bot.send_message(enemy_id, 
                                             text=i18n.enemy.damaged(),
                                             reply_markup=game_process_kb(i18n))
                try:
                    await bot.delete_message(enemy_id, msg.message_id - 1)

                except TelegramBadRequest:
                    await callback.answer()

                game[i_am + b'_health'] = int(str(game[i_am + b'_health'], encoding='utf-8')) - 1

            elif result == 'nobody_won':
     
                # Write result to Redis
                await r.set('result_'+str(user_id), result)

                try:
                    # Return result of turn and keyboard for next move
                    await callback.message.edit_text(text=i18n.nobody.won(),
                                                     reply_markup=game_process_kb(i18n))
                except TelegramBadRequest:
                    await callback.answer()
                
                # Return to opponent result of turn and keyboard for next move
                await asyncio.sleep(1)
                msg = await bot.send_message(enemy_id, 
                                             text=i18n.nobody.won(),
                                             reply_markup=game_process_kb(i18n))
                try:
                    wait = str(await r.get('wait_'+str(enemy_id)), encoding='utf-8')
                    await bot.delete_message(enemy_id, int(wait))
                except TelegramBadRequest:
                    await callback.answer()

            game[b'player1_move'] = b'0'
            game[b'player2_move'] = b'0'

            await r.hmset('g_'+str(room_id), game)

            # Checking player1 health for zero
            if game[b'player1_health'] == b'0' or game[b'player1_health'] == 0:
                if i_am == b'player1':
                    await game_result(callback, dialog_manager, 'lose',
                                      enemy_id, user_id, game, i18n, bot, game_end)
                else:
                    await game_result(callback, dialog_manager, 'win',
                                      enemy_id, user_id, game, i18n, bot, game_end)

            # Checking player2 health for zero
            elif game[b'player2_health'] == b'0' or game[b'player2_health'] == 0:
                if i_am == b'player2':
                    await game_result(callback, dialog_manager, 'lose',
                                      enemy_id, user_id, game, i18n, bot, game_end)
                else:
                    await game_result(callback, dialog_manager, 'win',
                                      enemy_id, user_id, game, i18n, bot, game_end)
        else:
            if game[b'player1_move'] == b'0' and game[b'player2_move'] == b'0':
                last_result = await r.get('result_'+str(user_id))
                result_map = {b'you_caused_damage': i18n.enemy.damaged(),
                              b'enemy_caused_damaged': i18n.you.damaged(),
                              b'nobody_won': i18n.nobody.won()}
                try: 
                    await callback.message.edit_text(text=result_map[last_result],
                                                     reply_markup=game_process_kb(i18n))
                except TelegramBadRequest:
                    await callback.answer()
            else:
                # Suggest you wait
                try:
                    wait = await callback.message.edit_text(text=i18n.choice.made())
                                                            #reply_markup=check_kb(i18n))
                    await r.set('wait_'+str(user_id), wait.message_id)
                except TelegramBadRequest:
                    await callback.answer()


# Canceling game before by Player
@router_game.callback_query(F.data == 'leave_game', 
                            StateFilter(GameSG.main)
                            )
async def process_end_game_button(callback: CallbackQuery,  
                                  state: FSMContext, 
                                  i18n: TranslatorRunner,
                                  dialog_manager: DialogManager,
                                  bot: Bot
                                  ):

    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    game_result = services.game_services.game_result
    user_id = callback.from_user.id
    room_id = str(await r.get(user_id), encoding='utf-8')
    _game = await r.hgetall('g_'+str(room_id))

    player1 = int(str(_game[b'player1'], encoding='utf-8'))
    player2 = int(str(_game[b'player2'], encoding='utf-8'))

    enemy_id = player1 if player1 != user_id else player2
    game = await r.hgetall('g_' + str(room_id))
    
    logger.info(f"User {user_id} leaved the game!")
    await game_result(callback, dialog_manager, 'lose',
                      enemy_id, user_id, game, i18n, bot, game_end)




