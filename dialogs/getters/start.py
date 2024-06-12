import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_nft_metadata
from database import users

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Getter for start menu
async def start_getter(
    dialog_manager: DialogManager,
    db_engine: AsyncEngine,
    i18n: TranslatorRunner,
    event_from_user: User,
    **kwargs
) -> dict[str, str]:

    logger.info('START button processing - start_getter')
    page: int  # Number of last item from User data

    # User ID
    user_dict = dialog_manager.start_data
    if user_dict is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    # Get page number
    statement = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(statement)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')

    item = await get_nft_metadata(page, db_engine)
    name = item['name']
    image = item['image']
    description = item['description']

    logger.info(f'NFT metadata for page:\n{name}\n{image}\n{description}')

    return {"button_back": i18n.button.back(),
            "button_next": i18n.button.next(),
            "button_want": i18n.button.want(),
            "button_account": i18n.button.account(),
            "button_catalogue": i18n.button.catalogue(),
            "name": name,
            "image": image,
            "description": description}
