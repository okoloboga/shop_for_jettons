from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row

from .getter import *
from .handler import *
from ..start import switch_to_edit_row, switch_to_catalogue


'''Show items with pagination'''
item_dialog = Dialog(
    Window(
        Format('{item_show}'),
        Button(Format('{button_delete_row}'), id='b_delete_row', on_click=switch_to_edit_row),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
        getter=start_previous_getter,
        state=ItemSG.start_previous
    ),
    Window(
        Format('{item_show}'),
        Button(Format('{button_delete_row}'), id='b_delete_row', on_click=switch_to_edit_row),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
        getter=start_next_getter,
        state=ItemSG.start_next
    ),
    Window(
        Format('{item_show}'),
        Button(Format('{button_delete_row}'), id='b_delete_row', on_click=switch_to_edit_row),
        Row(
            Button(Format('{button_back}'), id='b_back', on_click=previous_page),
            Button(Format('{button_next}'), id='b_next', on_click=next_page),
        ),
        Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
        getter=show_item_getter,
        state=ItemSG.show_item
    )
)
