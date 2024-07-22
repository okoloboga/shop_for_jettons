import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import TextInput, ManagedTextInput

from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import AddRowSG


router_add_row = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Adding Row process - start
async def add_row_start(
        callback: CallbackQuery,
        db_config: AsyncEngine,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} starts filling category')
    await dialog_manager.switch_to(AddRowSG.fill_category)


# Filling category of item
async def fill_category(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        category: str
):
    logger.info(f'User {callback.from_user.id} fills category: {category}')

    dialog_manager.current_context().dialog_data['category'] = category
    await dialog_manager.next()


# Wrong category
async def wrong_category(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.warning(f'User {callback.from_user.id} fills wrong category')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.category())


# Filling Item Name
async def fill_name(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        name: str
):
    logger.info(f'User {callback.from_user.id} fills name {name}')

    dialog_manager.current_context().dialog_data['name'] = name
    await dialog_manager.next()


# Wrong name
async def wrong_name(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.warning(f'User {callback.from_user.id} fills wrong category')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.name())


# Filling Item Description
async def fill_description(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        description: str
):
    logger.info(f'User {callback.from_user.id} fills description {description}')

    dialog_manager.current_context().dialog_data['description'] = description
    await dialog_manager.next()


# Wrong Description
async def wrong_description(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.info(f'User {callback.from_user.id} fills wrong description')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.description())


# Filling Image URL
async def fill_image(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        url: str
):
    logger.info(f'User {callback.from_user.id} fills image URL {url}')

    dialog_manager.current_context().dialog_data['image'] = url
    await dialog_manager.next()


# Wrong Image URL
async def wrong_image(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.info(f'User {callback.from_user.id} fills wrong image URL')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.image())


# Filling Sell price, Self price and Count of Items
async def fill_price_count(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        price_count: str
):
    logger.info(f'User {callback.from_user.id} fills sell price, self price and count of item {price_count}')

    price_count_list = price_count.split()
    sell_price = price_count_list[0]
    self_price = price_count_list[1]
    count = price_count_list[2]

    dialog_manager.current_context().dialog_data['sell_price'] = sell_price
    dialog_manager.current_context().dialog_data['self_price'] = self_price
    dialog_manager.current_context().dialog_data['count'] = count

    await dialog_manager.next()


# Wrong Sell price, Self price and count of Items
async def wrong_price_count(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.info(f'User {callback.from_user.id} fills wrong sell price, self price and count of item')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.price.count())


# Confirming filled total data of new item
async def confirm_new_item(
        callback: CallbackQuery,
        widget: TextInput,
        dialog_manager: DialogManager,
):
    logger.info(f'User {callback.from_user.id} confirm new item')
    await dialog_manager.next()










