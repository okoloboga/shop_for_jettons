from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from .getter import *
from .handler import *
from states import MainSG


dialog = Dialog(
    Window(
        Format('{fill_eth_address}'),
        TextInput(
            id='eth_address',
            type_factory=str,
            on_success=check_eth_address,
            on_error=wrong_input
        ),
        getter=eth_getter,
        state=MainSG.fill_eth
    ),
    Window(
        Format('{fill_sol_address}'),
        TextInput(
            id='sol_address',
            type_factory=str,
            on_success=check_sol_address,
            on_error=wrong_input
        ),
        getter=sol_getter,
        state=MainSG.fill_sol
    ),
    Window(
        Format('{select_coin}'),
        Button(Format('{button_eth}'), id='b_eth', on_click=select_eth),
        Row(
            Button(Format('{button_sol}'), id='b_sol', on_click=select_sol),
            Button(Format('{button_ftm}'), id='b_ftm', on_click=select_ftm)
        ),
        Button(Format('{button_account}'), id='b_account', on_click=account),
        getter=coin_getter,
        state=MainSG.select_coin
    ),
    Window(
        Format('{account}'),
        TextInput(
            id='new_address',
            type_factory=str,
            on_success=check_address,
            on_error=wrong_input
        ),
        Button(Format('{button_back}'), id='b_back', on_click=back),
        getter=account_getter,
        state=MainSG.account
    )    
)
