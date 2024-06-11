import pprint
import logging

from aiogram import html, Bot
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import insert, delete, select, column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services.services import get_nft_metadata
from services.ton_services import wallet_deploy
from database.tables import users, catalogue

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


"""Account"""


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


"""Catalogue"""


# Show catalogue - names of NFT's
async def catalogue_show(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    # Get all NFT for catalogue from database
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
            'nft_list': i18n.nft.list()}


# Processing switch to previous page
async def start_previous_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    logger.info(f'User {user_id} presser PREVIOUS button')

    page: int  # Current page of user from database
    new_page: int  # Users page after updating
    catalogue_len: int  # Number of items in catalogue

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    # Get number of items in catalogue
    count = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        count_raw = await conn.execute(count)
        for row in count_raw:
            catalogue_len = row[0]
            logger.info(f'{catalogue_len} items total in Catalogue')
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')

    if page == 0:
        # New page value, if current page is 0
        new_page = catalogue_len - 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    else:
        # New page value, if current page bigger than 0
        new_page = page - 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    # Getting data of NFT item from new Users page
    item = await get_nft_metadata(new_page, db_engine)
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


# Processing switch ot next page
async def start_next_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')
    user_id = user_dict['user_id']

    logger.info(f'User {user_id} presser NEXT button')

    page: int  # Current page of user from database
    new_page: int  # Users page after updating
    catalogue_len: int  # Number of items in catalogue

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    # Get number of items in catalogue
    count = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        count_raw = await conn.execute(count)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')
        for row in count_raw:
            catalogue_len = row[0]
            logger.info(f'{catalogue_len} items total in Catalogue')

    if page == catalogue_len - 1:
        # New page value, if current page is equal number of items in catalogue
        new_page = 0
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    else:
        # New page value, if current page is less than number of items in catalogue
        new_page = page + 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    # Getting data of NFT item from new Users page
    item = await get_nft_metadata(new_page, db_engine)
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


# Show selected item from catalogue
async def show_item_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
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

    # Getting data of NFT item from ITEM_ID
    item = await get_nft_metadata(int(item_id), db_engine)
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
