import logging

from aiogram.types import User
from fluentogram import TranslatorRunner

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Getter for start menu
async def start_getter(
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    logger.info('START button processing - start_getter')

    return {
        "button_back": i18n.button.back(),
        "button_add_row": i18n.button.add.row(),
        "button_orders": i18n.button.orders(),
        "button_catalogue": i18n.button.catalogue(),
        "start": i18n.start.admin()
    }
