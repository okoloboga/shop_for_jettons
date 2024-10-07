import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_user_data
from config import get_config, WalletConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Start getter - check for new user
# If user is New - fill ETH address
async def eth_getter(dialog_manager: DialogManager,
                     db_engine: AsyncEngine,
                     i18n: TranslatorRunner,       
                     event_from_user: User,
                     **kwargs
                     ) -> dict:
    
    name = event_from_user.first_name

    return {'fill_eth_address': i18n.fill.eth.address(name=name)}


# Offer to fill TRX address
async def trx_getter(dialog_manager: DialogManager,
                      db_engine: AsyncEngine,
                      i18n: TranslatorRunner,       
                      event_from_user: User,
                      **kwargs
                      ) -> dict:

    return {'fill_trx_address': i18n.fill.trx.address()}

'''
# Offeer to fill SOL address
async def sol_getter(dialog_manager: DialogManager,
                     db_engine: AsyncEngine,
                     i18n: TranslatorRunner,       
                     event_from_user: User,
                     **kwargs
                     ) -> dict:

    return {'fill_sol_address': i18n.fill.sol.address()}
'''

# Select Coin to get to wallet
async def coin_getter(dialog_manager: DialogManager,
                      db_engine: AsyncEngine,
                      i18n: TranslatorRunner,       
                      event_from_user: User,
                      **kwargs
                      ) -> dict:

    central_wallet = get_config(WalletConfig, 'wallet')

    return {'select_coin': i18n.select.coin(eth=central_wallet.ethQuote,
                                            ftm=central_wallet.ftmQuote,
                                            # sol=central_wallet.solQuote,
                                            trx=central_wallet.trxQuote),
            'button_eth': i18n.button.eth(),
            # 'button_sol': i18n.button.sol(),
            'button_ftm': i18n.button.ftm(),
            'button_trx': i18n.button.trx(),
            'button_account': i18n.button.account()}


# Account menu - offer to change addresses
async def account_getter(dialog_manager: DialogManager,
                         db_engine: AsyncEngine,
                         i18n: TranslatorRunner,       
                         event_from_user: User,
                         **kwargs
                         ) -> dict:

    user = event_from_user.id
    user_data = await get_user_data(user, db_engine)

    return {'account': i18n.account(**user_data),
            'button_back': i18n.button.back()}

    
