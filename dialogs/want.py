from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row

from states import WantSG
from dialogs import start_getter
from handlers import (go_start, switch_to_account, switch_to_catalogue)

'''Want Dialog'''
want_dialog = Dialog(
    Window(
        Const('WANT'),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_account}'), id='account', on_click=switch_to_account),
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=start_getter,
        state=WantSG.want
    )
)
