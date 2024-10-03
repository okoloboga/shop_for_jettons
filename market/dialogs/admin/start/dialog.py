from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row

from .getter import *
from .handler import *


admin_start_dialog = Dialog(
    Window(
        Format('{start}'),
        Button(Format('{button_add_row}'), id='b_add_row', on_click=switch_to_add_row),
        Row(
            Button(Format('{button_catalogue}'), id='b_catalogue', on_click=switch_to_catalogue),
            Button(Format('{button_orders}'), id='b_orders', on_click=switch_to_confirm_order)
        ),   
        Button(Format('{button_back}'), id='b_back', on_click=go_start_total),
        getter=start_getter,
        state=Admin_StartSG.main
    )
)