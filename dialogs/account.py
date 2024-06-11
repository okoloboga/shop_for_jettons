from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import TextInput

from states.states import StartSG, AccountSG, CatalogueSG, WantSG
from dialogs.getters import account_getter
from handlers.buttons import go_back, go_next
from handlers.switchers import *
from services.services import get_nft_metadata


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
