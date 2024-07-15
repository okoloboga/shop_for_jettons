import logging

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input.text import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from fluentogram import TranslatorRunner

from states import Admin_StartSG


router_account = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Cheking for admin after #admin_panel command
async def check_admin(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      text: str
                      ):
    user_id = callback.from_user.id
    logger.info(f'User {user_id} entered #admin_panel command')
    admins = dialog_manager.current_context().dialog_data['admins']
    
    # User is Admin?
    if user_id in admins:
        await dialog_manager.start(Admin_StartSG.main)        
    else:
        i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
        await callback.answer(text=i18n.unknown.message())

        

# Entered not #admin_panel
async def wrong_input(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      text: str
                      ):
    user_id = callback.from_user.id
    logger.info(f'User {user_id} entered wrong command')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.unknown.message())
    

# Show wallet address
async def show_address(callback: CallbackQuery,
                       button: Button,
                       dialog_manager: DialogManager
                       ):
    address = dialog_manager.current_context().dialog_data['address']
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.message.answer(text=i18n.wallet.address(address=address))
    
    