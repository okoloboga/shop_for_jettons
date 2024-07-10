from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.input.text import TextInput

from .getter import account_getter
from dialogs.buttons import switch_to_catalogue, go_start
from .handler import *
from states import AccountSG
from services import is_admin

'''Account Dialog'''
account_dialog = Dialog(
    # Main information
    Window(
        Format('{account_data}'),
        Row(
            Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_back}'), id='b_back', on_click=go_start),
        ),
        TextInput(
            id='admin_panel',
            type_factory=is_admin,
            on_success=check_admin,
            on_error=wrong_input
        ),
        getter=account_getter,
        state=AccountSG.account
    )
)
