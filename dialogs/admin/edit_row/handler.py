import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from fluentogram import TranslatorRunner

from states import EditRowSG


router_edit_row = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Edit Item process - Start
async def edit(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} starts editing item')
    await dialog_manager.switch_to(EditRowSG.edit)


# Delete Item process
async def delete(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} starts delete item')
    await dialog_manager.switch_to(EditRowSG.delete)


# Delete confirmed
async def delete_confirm(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    logger.info(f'User {callback.from_user.id} delete item')
    await dialog_manager.switch_to(EditRowSG.delete_confirmed)

    
# Filling changes confirmed
async def fill_changes(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        new_data: str | int
):
    logger.info(f'User {callback.from_user.id} filled changes: {new_data}')

    dialog_manager.current_context().dialog_data['new_data'] = new_data
    await dialog_manager.switch_to(EditRowSG.changes_confirmed)


# Wrong changes
async def wrong_changes(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        new_data: str | int
):
    logger.warning(f'User {callback.from_user.id} fills wrong changes')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.changes())
    


"""Edit Buttons"""


# Processing button Edit category
async def edit_category(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'category'
    logger.info(f'User {callback.from_user.id} edit category')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit name
async def edit_name(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'name'
    logger.info(f'User {callback.from_user.id} edit name')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit description
async def edit_description(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'description'
    logger.info(f'User {callback.from_user.id} edit description')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit image
async def edit_image(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'image'
    logger.info(f'User {callback.from_user.id} edit image')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit sellprice
async def edit_sellprice(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'sell_price'
    logger.info(f'User {callback.from_user.id} edit sellprice')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit selfprice
async def edit_selfprice(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'self_price'
    logger.info(f'User {callback.from_user.id} edit selfprice')
    await dialog_manager.switch_to(EditRowSG.new_data)
    
    
# Processing button Edit count
async def edit_count(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):  
    dialog_manager.current_context().dialog_data['change'] = 'count'
    logger.info(f'User {callback.from_user.id} edit count')
    await dialog_manager.switch_to(EditRowSG.new_data)














