from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from states import WantSG
from .getter import *
from .handler import *


"""Want dialog - for selling"""
want_dialog = Dialog(
    Window(
        Format('{item_information'),
        Button(Format('{button_take_it}'), id='b_take_it', on_click=take_it),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='account', on_click=switch_to_account),
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=item_info_getter,
        state=WantSG.want
    ),
    Window(
        Format('{fill_count}'),
        TextInput(
            id='fill_count',
            type_factory=str,
            on_success=fill_count,
            on_error=wrong_count
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_count_getter,
        state=WantSG.fill_count
    ),
    Window(
        Format('{fill_address}'),
        TextInput(
            id='fill_address',
            type_factory=str,
            on_success=fill_address,
            on_error=wrong_address
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_address_getter,
        state=WantSG.fill_address
    ),
    Window(
        Format('{buy_confirmation}'),
        Button(Format('{button_confirm}'), id='b_confirm', on_click=buy_confirm),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=buy_confirmation,
        state=WantSG.confirm
    )