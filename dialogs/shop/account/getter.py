import logging

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import (get_admins_list, get_user_account_data, 
                      get_token_balance)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Getter for Account menu
async def account_getter(dialog_manager: DialogManager,
                         db_engine: AsyncEngine,
                         i18n: TranslatorRunner,
                         bot: Bot,
                         event_from_user: User,
                         **kwargs
                         ) -> dict[str, str]:

    user_data: list  # Result list for user data

    # User ID
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    # Getting user info for display in Account dialog
    user_data = await get_user_account_data(user_id, db_engine)

    # Getting list of admins
    dialog_manager.current_context().dialog_data['admins'] = await get_admins_list(db_engine)
    
    # Referral link
    link = await create_start_link(bot, str(user_id), encode=True)

    # Getting value of tokens
    tokens = (await get_token_balance(user_data['address']))['data']

    dialog_manager.current_context().dialog_data['address'] = user_data['address']
    
    logger.info(f"User data\nPurchase: {user_data['purchase']}\nPurchase sum: {user_data['purchase_sum']}\n\
                Wallet address: {user_data['address']}\nReferrals: {user_data['referrals']}\n\
                Referral Link: {link}\nToken balance: {tokens}")

    return {"button_back": i18n.button.back(),
            "button_wallet": i18n.button.wallet(),
            "button_catalogue": i18n.button.catalogue(),
            "account_data": i18n.account.data(user_id=user_id,
                                              purchase=user_data['purchase'],
                                              purchase_sum=user_data['purchase_sum'],
                                              tokens=tokens,
                                              link=link,
                                              referrals=user_data['referrals'])}
