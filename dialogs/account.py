from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from .getters import account_getter
from handlers import switch_to_catalogue, go_start
from states import AccountSG

'''Account Dialog'''
account_dialog = Dialog(
    # Main information
    Window(
        Format('{account_data}'),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_back}'), id='b_back', on_click=go_start),
        ),
        getter=account_getter,
        state=AccountSG.account
    )
)
