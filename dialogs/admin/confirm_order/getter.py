import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.tables import users, orders
from services import (delete_item, change_item, get_order_data, get_orders_list)


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Showing statuses for select
async def select_status_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    return {'select_status': i18n.select.status(),
            'button_new_orders': i18n.button.new.orders(),
            'button_accepted_orders': i18n.button.accepted.orders(),
            'button_declined_orders': i18n.button.declined.orders(),
            'button_back': i18n.button.back()
    }


# Show orders from costumers
async def orders_list_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')

    status = dialog_manager.current_context().dialog_data['status']
    user_id = user_dict['user_id']
    
    orders_list = get_orders_list(db_engine,
                                  int(user_id),
                                  str(status))
    
    orders_indexes = [i[0] for i in orders_list]
    
    dialog_manager.current_context().dialog_data['orders_indexes'] = orders_indexes

    return {'orders_list': i18n.orders.list(),
            'orders': tuple(orders_list),
            'button_back': i18n.button.back()}
    
    
# Selected one of orders... Order information
async def order_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):  
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')

    user_id = user_dict['user_id']   
    order = dialog_manager.current_context().dialog_data['order']
    
    selected_order = get_order_data(db_engine, int(order))
            
    return {"button_decline": i18n.decline.order(),
            "button_confirm": i18n.button.confirm(),
            "button_complete_order": i18n.button.complete.order(),
            "button_accept_order": i18n.accept.order(),
            "button_decline_order": i18n.decline.order(),
            "button_back": i18n.button.back(),
            "new_selected_order": i18n.new.selected.order(index=order),
            "accept_order": i18n.accept.order(index=order),
            "decline_order": i18n.decline.order(index=order),
            "accepted_order": i18n.accepted.order(index=order),
            "declined_order": i18n.declined.order(index=order),
            "order_data": i18n.order.data(
                index=selected_order[0],
                user_id=selected_order[1],
                username=selected_order[2],
                delivery_address=selected_order[3],
                date_and_time=selected_order[4],
                item_index=selected_order[5],
                category=selected_order[6],
                name=selected_order[7],
                count=selected_order[8],
                income=selected_order[9],
                pure_income=selected_order[10],
                status=selected_order[11]
                )
            }




    
        
        
    
        
    


