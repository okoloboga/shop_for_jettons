from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row

from .getter import *
from .handler import *

'''Starting Menu with NFT'''
start_dialog = Dialog(
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
        getter=show_item_getter,
        state=StartSG.show_item
    )
)
