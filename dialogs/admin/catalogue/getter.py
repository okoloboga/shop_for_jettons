import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database import catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show list if items from catalogue
async def catalogue_show(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwarg
):
    # Get all items for catalogue from database
    statement = (
        select(column("name"), column("index")).select_from(catalogue)
    )
    async with db_engine.connect() as conn:
        catalogue_tuples = await conn.execute(statement)
        logger.info('Catalogue executed')

    # Bring it to list
    catalogue_list = []
    for item in catalogue_tuples:
        catalogue_list.append(item)
    logger.info(f'Catalogue list is {catalogue_list}')

    return {
            'catalogue_list': catalogue_list,
            'button_back': i18n.button.back(),
            'item_list': i18n.item.list()
           }
