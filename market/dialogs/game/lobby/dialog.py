from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Select, Group

from .getter import *
from .handler import *
from dialogs.game.game import game_confirm 
from states import LobbySG


lobby_dialog = Dialog(
    Window(
        Format('{lobby_menu}'),
        Button(Format('{button_play}'), id='b_play', on_click=lobby_play),
        Button(Format('{button_stats}'), id='b_stats', on_click=lobby_stats), # Show info in single message
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=lobby_menu_getter,
        state=LobbySG.main
    ),
    Window(
        Format('{create_join}'),
        Button(Format('{button_create_game}'), id='b_create_game', on_click=lobby_create),
        Button(Format('{button_join_game}'), id='b_join_game', on_click=lobby_join),
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=create_join_getter,
        state=LobbySG.create_join
        ),
    Window(
        Format('{make_bet}'),
        Row(
            Button(Format('{button_bet_1}'), id='b_bet_1', on_click=bet),
            Button(Format('{button_bet_2}'), id='b_bet_2', on_click=bet),
            Button(Format('{button_bet_3}'), id='b_bet_3', on_click=bet),
            ),
        Row(
            Button(Format('{button_bet_4}'), id='b_bet_4', on_click=bet),
            Button(Format('{button_bet_5}'), id='b_bet_5', on_click=bet),
            ),
        Button(Format('{button_bet_25}'), id='b_bet_25', on_click=bet),
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=make_bet_getter,
        state=LobbySG.make_bet
        ),
    Window(
        Format('{waiting_game}'),
        Button(Format('{button_wait}'), id='b_wait', on_click=wait_game),
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=waiting_game_getter,
        state=LobbySG.wait_game
        ),
    Window(
        Format('{search_game}'),
        Group(
            Select(
                Format('{item[0]} - {item[1]}'),
                id='rooms',
                item_id_getter=lambda x: x,
                items='rooms_list',
                on_click=game_selection
                ),
            width=1
            ),
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=search_game_getter,
        state=LobbySG.select_enemy
        ),
    Window(
        Format('{game_confirm}'),
        Button(Format('{button_game_confirm}'), id='b_game_confirm', on_click=game_confirm),
        getter=game_confirm_getter,
        state=LobbySG.game_confirm
        )
    )


