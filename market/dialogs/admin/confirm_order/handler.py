import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Button

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from fluentogram import TranslatorRunner

from states import ConfirmOrderSG

router_confirm_order = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Status New selected
async def new_orders(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager,
                     ):

    logger.info(f'User {callback.from_user.id} watching for NEW order')
    dialog_manager.current_context().dialog_data['status'] = 'new'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)
 
 
# Status Accepted selected
async def accepted_orders(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager,
                          ):

    logger.info(f'User {callback.from_user.id} watching for ACCEPTED orders')
    dialog_manager.current_context().dialog_data['status'] = 'accepted'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order) 


# Status Declined selected
async def declined_orders(callback: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager,
                          ):

    logger.info(f'User {callback.from_user.id} watching for DECLINED orders')
    dialog_manager.current_context().dialog_data['status'] = 'declined'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)
    

# Selecting order from list with saved status
async def select_order(callback: CallbackQuery,
                       widget: ManagedTextInput, 
                       dialog_manager: DialogManager,
                       order: str
                       ):

    status = dialog_manager.current_context().dialog_data['status']
    dialog_manager.current_context().dialog_data['order'] = order
    logger.info(f'User {callback.from_user.id} select {order} of {status}')
    
    orders_indexes = dialog_manager.current_context().dialog_data['orders_indexes']
    logger.info(f'Orders Indexes: {orders_indexes}')
    logger.info(f'Order[1:] {order[1:]}')
                
    if int(order[1:]) in orders_indexes:    
        logger.info(f'Order {order[1:]} in orders_indexes {orders_indexes}')
            
        if status == 'new':
            await dialog_manager.switch_to(ConfirmOrderSG.new_order)
            
        elif status == 'accepted':
            await dialog_manager.switch_to(ConfirmOrderSG.accepted_order)
            
        elif status == 'declined':
            await dialog_manager.switch_to(ConfirmOrderSG.declined_order)
            
        elif status == 'completed':
            await dialog_manager.switch_to(ConfirmOrderSG.completed_order)
    else:
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        await callback.answer(text=i18n.wrong.order())
    
    

# Filled wrong order
async def wrong_order(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      text_input: TextInput
                      ):

    logger.warning(f'User {callback.from_user.id} fills wrong order')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.order())


# Accepting order
async def accept_order(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager
                       ):  

    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} accepting order {order}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    await callback.answer(text=i18n.accepting.order(
                                    order=order
                                )
                          )
    await dialog_manager.switch_to(ConfirmOrderSG.accept_order)


# Declining order
async def decline_order(callback: CallbackQuery,
                        button: Button,
                        dialog_manager: DialogManager
                        ):

    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} declining order {order}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    await callback.answer(text=i18n.declining.order(
                                    order=order
                                )
                          )
    await dialog_manager.switch_to(ConfirmOrderSG.decline_order)
    

# Confirming order accept
async def confirm_accept_order(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager
                               ):

    user_id = callback.from_user.id
    order = dialog_manager.current_context().dialog_data['order']
    dialog_manager.current_context().dialog_data['updated_status'] = 'accepted'
    
    logger.info(f'User {user_id} confirm accept order {order}')
    
    await dialog_manager.switch_to(ConfirmOrderSG.status_changed)


# Confirming order decline
async def confirm_decline_order(callback: CallbackQuery,
                                widget: ManagedTextInput,
                                db_engine: AsyncEngine,
                                dialog_manager: DialogManager,
                                reason: str
                                ):

    dialog_manager.current_context().dialog_data['reason'] = reason
    dialog_manager.current_context().dialog_data['updated_status'] = 'declined'
    
    await dialog_manager.switch_to(ConfirmOrderSG.status_changed) 
    

# Filled wrong reason 
async def wrong_reason(callback: CallbackQuery,
                       widget: ManagedTextInput,
                       dialog_manager: DialogManager,
                       text_input: TextInput
                       ):

    logger.info(f'User {callback.from_user.id} fills wrong reason')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.reason())
    
    
# Complete order that in process
async def complete_order(callback: CallbackQuery,
                         button: Button,
                         dialog_manager: DialogManager
                         ):

    dialog_manager.current_context().dialog_data['updated_status'] = 'completed'
  
    await dialog_manager.switch_to(ConfirmOrderSG.status_changed)

