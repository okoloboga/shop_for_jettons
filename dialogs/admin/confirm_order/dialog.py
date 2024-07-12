from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, List
from aiogram_dialog.widgets.kbd import Button

from .getter import *
from .handler import *
from ..start import go_start
from services import check_order


"""Confirming orders"""
confirm_order_dialog = Dialog(
    Window(
        Format('{select_status}'),
        Button(Format('{button_new_orders}'), id='b_new_orders', on_click=new_orders),
        Button(Format('{button_accepted_orders}'), id='b_accepted_orders', on_click=accepted_orders),
        Button(Format('{button_declined_orders}'), id='b_declined_orders', on_click=declined_orders),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=select_status_getter,
        state=ConfirmOrderSG.select_status        
    ),
    Window(
        Format('{orders_list}'),
        List(field=Format('<b>#{item[0]}</b> {item[1]} {item[2]} {item[3]}'),
             items='orders'),
        TextInput(
            id='select_order',
            type_factory=check_order,
            on_success=select_order,
            on_error=wrong_order
            ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=orders_list_getter,
        state=ConfirmOrderSG.select_order
    ),
    Window(
        Format('{new_selected_order}'),
        Format('{order_data}'),       
        Button(Format('{button_accept_order}'), id='b_accept_order', on_click=accept_order),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        Button(Format('{button_decline_order}'), id='b_decline_order', on_click=decline_order),
        getter=order_getter,
        state=ConfirmOrderSG.new_order
    ),
    Window(
        Format('{accept_order}'),
        Format('{order_data}'),
        Button(Format('{button_confirm}'), 
                      id='b_confirm', 
                      on_click=confirm_accept_order),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=order_getter,
        state=ConfirmOrderSG.accept_order
    ),
    Window(
        Format('{decline_order}'),
        Format('{order_data}'),   
        TextInput(
            id='decline_order',
            type_factory=str,
            on_success=confirm_decline_order,
            on_error=wrong_reason
            ), 
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=order_getter,
        state=ConfirmOrderSG.decline_order
    ),
    Window(
        Format('{accepted_order}'),
        Format('{order_data}'),
        Button(Format('{button_complete_order}'), id='b_complete_order', on_click=complete_order),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        Button(Format('{button_decline_order}'), id='b_decline_order', on_click=decline_order),
        getter=order_getter,
        state=ConfirmOrderSG.accepted_order
    ),
    Window(
        Format('{declined_order}'),
        Format('{order_data}'),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=order_getter,
        state=ConfirmOrderSG.declined_order
    )
)
