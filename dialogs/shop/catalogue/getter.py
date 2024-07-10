import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_user_item_metadata
from database import users, catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show catalogue - names of Items
async def catalogue_show(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:

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

    return {'catalogue_list': catalogue_list,
            'button_back': i18n.button.back(),
            'item_list': i18n.item.list()}


# Show selected item from catalogue
async def show_item_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
) -> dict[str, str]:
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')

    user_id = user_dict['user_id']
    item_id = user_dict['item_id']

    logger.info(f'User {user_id} select item №{item_id} from catalogue')

    # Rewrite User page to ITEM_ID
    update_page = (users.update()
                   .values(page=item_id)
                   .where(users.c.telegram_id == user_id)
                   )
    # Commit to database
    async with db_engine.connect() as conn:
        await conn.execute(update_page)
        await conn.commit()
        logger.info(f'Users {user_id} page is updated to {item_id}')

    # Getting data of item from ITEM_ID
    item = await get_user_item_metadata(int(item_id), db_engine)
    name = item['name']
    image = item['image']
    sell_price = item['sell_price']

    logger.info(f'Item metadata for page:\n{name}\n{image}\n{sell_price}')

    return {"button_back": i18n.button.back(),
            "button_next": i18n.button.next(),
            "button_want": i18n.button.want(),
            "button_account": i18n.button.account(),
            "button_catalogue": i18n.button.catalogue(),
            "name": name,
            "image": image,
            "sell_price": sell_price}
