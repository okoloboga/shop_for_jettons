import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import (get_user_item_metadata, get_user_account_data,
                          new_order, jetton_value, ton_value)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show more information about item
async def item_info_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

    page: int  # Current page of user from database

    # User ID
    user_dict = dialog_manager.start_data
    costumers_dict = await get_user_account_data(user_dict['user_id'],
                                                 db_engine)
    wallet = costumers_dict['address']    
    
    # Write jettons and TON value to dialog data
    dialog_manager.current_context().dialog_data['jettons'] = await jetton_value(wallet)
    dialog_manager.current_context().dialog_data['ton'] = await ton_value(wallet)
    dialog_manager.current_context().dialog_data['wallet'] = wallet

    # Getting data of item by Page in Users table
    item = await get_user_item_metadata(user_dict, db_engine)

    category = item['category']
    name = item['name']
    description = item['description']
    image = item['image']
    sell_price = item['sell_price']

    # Write to dialog data value of items in catalogue and it's price
    dialog_manager.current_context().dialog_data['current_count'] = item['count']
    dialog_manager.current_context().dialog_data['sell_price'] = item['sell_price']

    logger.info(f'Item metadata for page:\n{name}\n{sell_price}')

    return {
        "button_back": i18n.button.back(),
        "button_take_it": i18n.button.take.it(),
        "button_account": i18n.button.account(),
        "button_catalogue": i18n.button.catalogue(),
        "item_info": i18n.item.info(
            category=category,
            name=name,
            description=description,
            sell_price=sell_price
        ),
        "image": image
    }


# Switching to Fill count
async def fill_count_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

    return {
        "fill_count": i18n.fill.count(),
        "button_back": i18n.button.back()
    }


# Switching to Fill count
async def fill_address_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

    return {
        "fill_address": i18n.fill.address(),
        "button_back": i18n.button.back()
    }


# Order confirmation
async def order_confirmation_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    new_order_data = dialog_manager.current_context().dialog_data

    page: int  # Current page of user from database

    # User data
    user_dict = dialog_manager.start_data
    if user_dict['username'] is None:
        username = 'no_username'
    else:
        username = user_dict['username']

    # Getting data of item from PAGE
    item = await get_user_item_metadata(user_dict, 
                                        db_engine)

    category = item['category']
    name = item['name']
    description = item['description']
    image = item['image']
    sell_price = item['sell_price']

    dialog_manager.current_context().dialog_data['order_metadata'] = item

    return{
        "order_confirmation": i18n.order.confirmation(
            username=username,
            address=new_order_data['address'],
            category=category,
            name=name,
            description=description,
            sell_price=sell_price,
            count=new_order_data['count'],
            total_sum=int(new_order_data['count']) * sell_price
        ),
        "image": image,
        "button_great": i18n.button.great(),
        "button_back": i18n.button.back()
    }


# Complete order
async def complete_order_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    user_dict = dialog_manager.start_data
    new_order_data = dialog_manager.current_context().dialog_data
    
    logger.info(f'New Order Data: {new_order_data}')

    # Getting variables
    current_count = int(dialog_manager.current_context().dialog_data['current_count'])
    ton_value = dialog_manager.current_context().dialog_data['ton']
    wallet = dialog_manager.current_context().dialog_data['wallet']

    logger.info(f'TON Value of wallet {wallet} is {round(ton_value, 2)}')

    if round(ton_value, 2) > 0.065:
        # Place new order and return index of order
        index_and_data = await new_order(
            db_engine,
            i18n,
            user_dict,
            new_order_data,
            current_count
        )

        return {
            "result": i18n.order.complete(
                index=index_and_data[0],
                date_and_time=index_and_data[1]
            ),
            "button_catalogue": i18n.button.catalogue(),
            "button_account": i18n.button.account(),
            "button_back": i18n.button.back()
        }
    else:
        return {
            "result": i18n.notenough.ton(
                wallet=wallet
            ),
            "button_catalogue": i18n.button.catalogue(),
            "button_account": i18n.button.account(),
            "button_back": i18n.button.back()
        }

