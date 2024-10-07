import logging

from math import floor
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import TextInput, ManagedTextInput

from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from states import WantSG
from services import get_token_price


router_want = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# User pressed button TAKE IT ot start order process
async def take_it(callback: CallbackQuery,
                  button: Button,
                  dialog_manager: DialogManager):

    logger.info(f'User {callback.from_user.id} starts TAKE IT process')
    await dialog_manager.switch_to(WantSG.fill_count)


# Starts filling count of item
async def fill_count(callback: CallbackQuery,
                     widget: ManagedTextInput,
                     dialog_manager: DialogManager,
                     count: int):

    # Getting count of items from catalogue table
    current_count = int(dialog_manager.current_context()
                        .dialog_data['current_count'])

    logger.info(f'User {callback.from_user.id} fills count: {count}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    # Enough tokens in wallet?
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')
    token_price = await get_token_price(db_engine)
    price = dialog_manager.current_context().dialog_data['sell_price'] * token_price
    users_tokens = dialog_manager.current_context().dialog_data['tokens']
    total_order_sum = price * count
    
    if count > current_count:
        logger.info(f'Not enough items in catalogue! Asked {count}, total {current_count}')
        await callback.answer(text=i18n.too.large.count())
        
    elif total_order_sum > floor(users_tokens):
        logger.info(f'Not enough tokens! Need {total_order_sum}, user have {floor(users_tokens)}')
        await callback.answer(text=i18n.notenough.tokens(total_order_sum=total_order_sum,
                                                          tokens=users_tokens
        ))
    else:
        dialog_manager.current_context().dialog_data['count'] = count
        await dialog_manager.next()


# Wrong count
async def wrong_count(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      text_input: TextInput):

    logger.warning(f'User {callback.from_user.id} fills wrong count')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.count())


# Filling delivery address
async def fill_address(callback: CallbackQuery,
                       widget: ManagedTextInput,
                       dialog_manager: DialogManager,
                       address: str):

    logger.info(f'User {callback.from_user.id} fills count: {address}')

    dialog_manager.current_context().dialog_data['address'] = address
    await dialog_manager.next()


# Wrong address
async def wrong_address(callback: CallbackQuery,
                        widget: ManagedTextInput,
                        dialog_manager: DialogManager,
                        text_input: TextInput):

    logger.warning(f'User {callback.from_user.id} fills wrong address')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.address())


# Confirm order
async def order_confirm(callback: CallbackQuery,
                        widget: TextInput,
                        dialog_manager: DialogManager):
                        
    logger.info(f'User {callback.from_user.id} confim new order')
    await dialog_manager.next()
