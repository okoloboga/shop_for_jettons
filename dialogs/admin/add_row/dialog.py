from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button

from services import check_price_count, check_url
from .getter import *
from .handler import *
from ..start import go_start



add_row_dialog = Dialog(
    Window(
        Format('{add_row_main}'),
        Button(Format('{button_add_row}'), id='b_add_row', on_click=add_row_start),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=add_row_getter,
        state=AddRowSG.add_row
    ),
    Window(
        Format('{fill_category}'),
        TextInput(
            id='fill_category',
            type_factory=str,
            on_success=fill_category,
            on_error=wrong_category
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_category_getter,
        state=AddRowSG.fill_category
    ),
    Window(
        Format('{fill_name}'),
        TextInput(
            id='fill_name',
            type_factory=str,
            on_success=fill_name,
            on_error=wrong_name
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_name_getter,
        state=AddRowSG.fill_name
    ),
    Window(
        Format('{fill_description}'),
        TextInput(
            id='fill_description',
            type_factory=str,
            on_success=fill_description,
            on_error=wrong_description
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_description_getter,
        state=AddRowSG.fill_description
    ),
    Window(
        Format('{fill_image}'),
        TextInput(
            id='fill_image',
            type_factory=check_url,
            on_success=fill_image,
            on_error=wrong_image
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_image_getter,
        state=AddRowSG.fill_image
    ),
    Window(
        Format('{fill_price_count}'),
        TextInput(
            id='fill_price_count',
            type_factory=check_price_count,
            on_success=fill_price_count,
            on_error=wrong_price_count
        ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=fill_price_count_getter,
        state=AddRowSG.fill_price_count
    ),
    Window(
        Format('{confirm_new_item}'),
        Button(Format('{button_confirm}'), id='b_confirm', on_click=confirm_new_item),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=confirm_new_item_getter,
        state=AddRowSG.confirm
    ),
    Window(
        Format('{item_complete}'),
        Button(Format('{button_add_row}'), id='b_add_row', on_click=add_row_start),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=complete_new_item_getter,
        state=AddRowSG.complete
    )
)