from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row

from states import Admin_StartSG
from .getter import *
from .handler import *


admin_start_dialog = Dialog(
    Window(
        Format('{start}'),
        Button(Format('{button_add_row}'), id='b_add_row', on_click=switch_to_add_row),
        Button(Format('{button_catalogue}'), id='b_catalogue', on_click=switch_to_catalogue),
        Button(Format('{button_orders}'), id='b_orders', on_click=switch_to_confirm_order),
        getter=start_getter,
        state=Admin_StartSG.main
    )
)