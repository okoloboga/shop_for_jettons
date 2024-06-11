from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row, Select, Group

from states.states import StartSG, AccountSG, CatalogueSG, WantSG
from dialogs.getters import start_getter, catalogue_show
from handlers.buttons import go_back, go_next
from handlers.switchers import item_selection
from services.services import get_nft_metadata


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
