import logging

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database import users
from services import get_admins_list

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Getter for Account menu
async def account_getter(
    dialog_manager: DialogManager,
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

    # Read users data from database
    statement = (
        select("*")
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )
    async with db_engine.connect() as conn:
        user_data_raw = await conn.execute(statement)
        for row in user_data_raw:
            user_data = list(row)
        logger.info(f'Statement\n{user_data}\nexecuted of user {user_id}')

    # Getting list of admins
    dialog_manager.current_context().dialog_data['admins'] = await get_admins_list(db_engine)
    
    purchase = user_data[5]
    purchase_sum = user_data[6]
    address = user_data[3]
    referrals = user_data[7]
    link = await create_start_link(bot, str(user_id), encode=True)

    logger.info(f'User data\nPurchase: {purchase}\nPurchase sum: {purchase_sum}\nWallet address: {address}\nReferrals: {referrals}\nLink: {link}')

    return {"button_back": i18n.button.back(),
            "button_referral": i18n.button.referral(),
            "button_catalogue": i18n.button.catalogue(),
            "account_data": i18n.account.data(user_id=user_id,
                                              purchase=purchase,
                                              purchase_sum=purchase_sum,
                                              address=address,
                                              link=link,
                                              referrals=referrals)}
