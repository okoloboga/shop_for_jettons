from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row

from .getter import *
from .handler import *
from dialogs.buttons import go_start, switch_to_account, switch_to_catalogue, switch_to_want
from dialogs.game import process_start_command

'''Starting Menu with Items'''
start_dialog = Dialog(
    Window(
        Format('{item_show}'),
        StaticMedia(
            url=Format('{image}'),
            type=ContentType.PHOTO
        ),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_want}'), id='b_want', on_click=switch_to_want),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Row(
            Button(Format('{button_catalogue}'), id='b_catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='b_account', on_click=switch_to_account),
        ),
        Button(Format('{button_game}'), id='b_game', on_click=process_start_command),
        getter=start_getter,
        state=StartSG.start
    ),
    Window(
        Format('{item_show}'),
        StaticMedia(
            url=Format('{image}'),
            type=ContentType.PHOTO
        ),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_want}'), id='want', on_click=switch_to_want),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='account', on_click=switch_to_account),
        ),
        Button(Format('{button_game}'), id='b_game', on_click=process_start_command),
        getter=start_previous_getter,
        state=StartSG.start_previous
    ),
    Window(
        Format('{item_show}'),
        StaticMedia(
            url=Format('{image}'),
            type=ContentType.PHOTO
        ),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_want}'), id='want', on_click=switch_to_want),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='account', on_click=switch_to_account),
        ),
        Button(Format('{button_game}'), id='b_game', on_click=process_start_command),
        getter=start_next_getter,
        state=StartSG.start_next
    ),
    Window(
        Format('{item_show}'),
        StaticMedia(
            url=Format('{image}'),
            type=ContentType.PHOTO
        ),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_want}'), id='want', on_click=switch_to_want),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='account', on_click=switch_to_account),
        ),
        Button(Format('{button_game}'), id='b_game', on_click=process_start_command),
        getter=show_item_getter,
        state=StartSG.show_item
    )
)
