import asyncio

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from fluentogram import TranslatorRunner
from redis import asyncio as aioredis

from ..keyboards import (back_kb, create_join_kb, select_enemy, game_process_kb,
                                 bet_kb, play_account_kb, game_confirm)
from states import FSMMain
from ..filters.filters import IsEnemy
from services import timer

router_game_lobby = Router()

"""GAME LOBBY: CREATE OR JOIN"""


# CREATE button pressing
@router_game_lobby.callback_query(F.data == 'create', 
                                  StateFilter(default_state)
                                  )
async def process_create_button(callback: CallbackQuery, 
                                state: FSMContext, 
                                i18n: TranslatorRunner
                                ):
    r = aioredis.Redis(host='localhost', port=6379)
    user = await r.hgetall(str(callback.from_user.id))

    # Checking for existing games of this player
    if user[b'current_game'] != b'0':
        try:
            await callback.message.edit_text(text=i18n.already.ingame(),
                                             reply_markup=play_account_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()
    else:
        try:
            await callback.message.edit_text(text=i18n.bet(),
                                             reply_markup=bet_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()
        await state.set_state(FSMMain.make_bet)


# BET selected by pressing button
@router_game_lobby.callback_query(F.data.in_(['b1', 'b2', 'b3', 'b4', 'b5', 'b25']), 
                                  StateFilter(FSMMain.make_bet)
                                  )
async def process_yes_answer(callback: CallbackQuery, 
                             state: FSMContext, 
                             i18n: TranslatorRunner
                             ):
    r = aioredis.Redis(host='localhost', port=6379)

    # Parsing for value of bet
    bet = int(callback.data[1]) if len(callback.data) != 3 else int(callback.data[1:3])

    user = await r.hgetall(str(callback.from_user.id))

    # If player have not enough jettons
    if bet > int(str(user[b'jettons'], encoding='utf-8')):
        await callback.message.edit_text(text=i18n.notenough(),
                                         reply_markup=bet_kb(i18n))
    else:

        # Creating new room
        await r.set('r_'+str(callback.from_user.id), bet)

        # Setting flag of waiting for game
        user[b'current_game'] = callback.from_user.id
        user[b'last_message'] = callback.message.message_id
        await r.hmset(str(callback.from_user.id), user)
        try:
            await callback.message.edit_text(text=i18n.yes.wait(),
                                             reply_markup=back_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()
        await state.set_state(FSMMain.wait_game)


# WAIT button pressing
@router_game_lobby.callback_query(F.data == 'wait', 
                                  StateFilter(FSMMain.wait_game)
                                  )
async def process_wait_button(callback: CallbackQuery, 
                              state: FSMContext, 
                              i18n: TranslatorRunner
                              ):
    r = aioredis.Redis(host='localhost', port=6379)

    # Checking for update of game start
    if await r.exists('g_'+str(callback.from_user.id)) != 0:
        try:
            await callback.message.edit_text(text=i18n.rules(),
                                             reply_markup=game_process_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()
        await state.set_state(FSMMain.in_game)
    else:
        try:
            await callback.message.edit_text(text=i18n.still.wait(),
                                             reply_markup=back_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()


# JOIN button pressing
@router_game_lobby.callback_query(F.data == 'join', 
                                  StateFilter(default_state)
                                  )
async def process_yes_answer(callback: CallbackQuery, 
                             state: FSMContext, 
                             i18n: TranslatorRunner
                             ):
    r = aioredis.Redis(host='localhost', port=6379)

    user = await r.hgetall(str(callback.from_user.id))
    rooms = {}
    for key in await r.keys("r_*"):
        rooms.update({str(key, encoding='utf-8'): str(await r.get(key), encoding='utf-8')})

    # Checking for existing games of this player
    if user[b'current_game'] != b'0':
        try:
            await callback.message.edit_text(text=i18n.already.ingame(),
                                             reply_markup=play_account_kb(i18n))
        except TelegramBadRequest:
            await callback.answer()
    else:

        # If no games, MAYBE: await r.scan_iter("prefix:g_")
        if len(rooms) == 0:
            try:
                await callback.message.edit_text(text=i18n.you.first(),
                                                 reply_markup=create_join_kb(i18n))
            except TelegramBadRequest:
                await callback.answer()
        else:
            try:
                await callback.message.edit_text(text=i18n.select.enemy(),
                                                 reply_markup=select_enemy(rooms, i18n))
            except TelegramBadRequest:
                await callback.answer()
            await state.set_state(FSMMain.select_enemy)


# Checking update for Enemy base (enemy+space+bet_value)
@router_game_lobby.callback_query(IsEnemy(), 
                                  StateFilter(FSMMain.select_enemy)
                                  )
async def select_enemy_button(callback: CallbackQuery, 
                              bot: Bot, 
                              state: FSMContext, 
                              i18n: TranslatorRunner
                              ):
    r = aioredis.Redis(host='localhost', port=6379)

    # Vars initialization
    space = callback.data.find(' ')
    id = callback.data[:space]
    bet = int(callback.data[space+1:])
    user = await r.hgetall(str(callback.from_user.id))
    enemy = await r.hgetall(id)
    rooms = {}
    for key in await r.keys("r_*"):
        rooms.update({str(key, encoding='utf-8'): str(await r.get(key), encoding='utf-8')})

    # Player select himself
    if int(callback.from_user.id) == int(id):
        try:
            await callback.message.edit_text(text=i18n.self(),
                                             reply_markup=select_enemy(rooms, i18n))
        except TelegramBadRequest:
            await callback.answer()

    # Chosen game ended or started with another player already
    elif await r.exists(id) == b'0':
        try:
            await callback.message.edit_text(text=i18n.no.game(),
                                             reply_markup=select_enemy(rooms, i18n))
        except TelegramBadRequest:
            await callback.answer()

    # Player have not enough jettons to make current bet
    elif bet > int(str(user[b'jettons'], encoding='utf-8')):
        try:
            await callback.message.edit_text(text=i18n.notenough(),
                                             reply_markup=select_enemy(rooms, i18n))
        except TelegramBadRequest:
            await callback.answer()

    # All is great, game starts
    else:
        room_id = callback.data[0:(callback.data.find(' '))]
        user[b'current_game'] = room_id
        await r.hmset(str(callback.from_user.id), user)
        game = {room_id: 'player1',
                callback.from_user.id: 'player2',
                'player1': room_id,
                'player2': callback.from_user.id,
                'bet': rooms['r_'+str(room_id)],
                'player1_move': 0,
                'player2_move': 0,
                'player1_health': 2,
                'player2_health': 2,
                'player1_msg_id': 0,
                'player2_msg_id': 0}
        await r.hmset('g_'+str(room_id), game)

        # Deleting waiting/lobby room
        await r.delete('r_'+str(room_id))

        try:
            msg2 = await callback.message.edit_text(text=i18n.rules(),
                                             reply_markup=game_process_kb(i18n))
            user[b'last_message'] = msg2.message_id
        except TelegramBadRequest:
            await callback.answer()
        await r.hmset(str(callback.from_user.id), user)
        await state.set_state(FSMMain.in_game)

        # Bot sends message to opponent for start game

        try:
            mes_id = int(str(enemy[b'last_message'], encoding='utf-8'))
            msg1 = await bot.send_message(chat_id=room_id,
                                          text=i18n.game.confirm(),
                                          reply_markup=game_confirm(i18n))
            await bot.delete_message(room_id, mes_id)
            enemy[b'last_message'] = msg1.message_id
            print(msg1.message_id)
            await r.hmset(room_id, enemy)
        except TelegramBadRequest:
            await callback.answer()

        await asyncio.create_task(timer(bot, i18n, room_id))

