from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Select, Group

from states import CatalogueSG
from .getters import catalogue_show
from handlers import item_selection

'''Catalogue Dialog'''
catalogue_dialog = Dialog(
    Window(
        Format('{nft_list}'),
        Group(
            Select(
                Format('{item[0]}'),
                id='catalogue',
                item_id_getter=lambda x: x[1],
                items='catalogue_list',
                on_click=item_selection
            ),
            width=1
        ),
        getter=catalogue_show,
        state=CatalogueSG.catalogue
    )
)
