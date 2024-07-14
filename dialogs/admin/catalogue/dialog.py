from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Group, Button

from states import Admin_CatalogueSG
from .getter import *
from .handler import *
from ..start import go_start

'''Catalogue Dialog'''
admin_catalogue_dialog = Dialog(
    Window(
        Format('{item_list}'),
        Group(
            Select(
                Format('{item[0]}'),
                id='catalogue',
                item_id_getter=lambda x: x[1],
                items='catalogue_list',
                on_click=item_selection
            ),
            width=2
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=catalogue_show,
        state=Admin_CatalogueSG.catalogue
    )
)
