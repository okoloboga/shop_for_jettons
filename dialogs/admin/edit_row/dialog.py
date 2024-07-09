from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from states import EditRowSG

from .getter import *
from .handler import *
from ..start import go_start
from services import check_changes


'''Item selected for editing'''
edit_dialog = Dialog(
    Window(
        Format('{item_show}'),
        Button(Format('{button_edit}'), id='b_edit', on_click=edit),
        Button(Format('{button_delete}'), id='b_delete', on_click=delete),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=edit_delete_getter,
        state=EditRowSG.edit_row
    ),
    Window(
        Format('{delete_confirm}'),
        Button(Format('{button_confirm}'), id='b_confirm', on_click=delete_confirm),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=edit_delete_getter,
        state=EditRowSG.delete
    ),
    Window(
        Format('{edit_menu}'),
        TextInput(
            id='fill_changes',
            type_factory=check_changes,
            on_success=fill_changes,
            on_error=wrong_changes
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=edit_delete_getter,
        state=EditRowSG.edit
    ),
    Window(
        Format('{delete_complete}'),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=delete_confirmed_getter,
        state=EditRowSG.delete_confirmed
    ),
    Window(
        Format('{changes_complete}'),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=changes_confirmed_getter,
        state=EditRowSG.changes_confirmed
    )
)