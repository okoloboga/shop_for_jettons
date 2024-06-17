import logging

from datetime import datetime
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from sqlalchemy import insert, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from fluentogram import TranslatorRunner

from database import users, catalogue, orders, variables
from config import get_config, BotConfig
from .ton_services import wallet_deploy

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# New User creating after first /START pressing
async def new_user(
        db_engine: AsyncEngine,
        user_id: int,
        first_name: str,
        last_name: str,
        payload: str | None
):
    logger.info('new_user processing')

    # Wallet data
    new_wallet = await wallet_deploy()
    new_address = new_wallet[0]
    logger.info(f'New wallet address is {new_address}')
    new_mnemonics = ' '.join(new_wallet[1])

    # If new user invited with referral link, and it is not himself
    if payload and payload != user_id:
        invited = 1

        logger.info(f'User {user_id} starts bot with referral link. Parent: {payload}')
        # Update referral parent by ID in payload
        update_parent = (users.update()
                         .values(referrals=users.c.referrals + 1)
                         .where(users.c.telegram_id == int(payload))
                         )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_parent)
            await conn.commit()
            logger.info(f'Users {payload} referrals are updated')

    # If user and referral parent is a one person
    elif payload and payload == user_id:
        invited = 0
        logger.warning(f'User {user_id} tries to invite himself. Payload {payload}')

    # No referral link
    else:
        invited = 0
        logger.info(f'User {user_id} starts bot without referral link')

    # New user statement for database
    new_user = insert(users).values(
        telegram_id=user_id,
        first_name=first_name,
        last_name=last_name,
        address=new_address,
        mnemonics=new_mnemonics,
        purchase=0,
        purchase_sum=0,
        referrals=0,
        invited=invited,
        page=0,
        status='user'
    )

    # If user already exists in database
    do_ignore = new_user.on_conflict_do_nothing(index_elements=["telegram_id"])

    # Commit to Database
    async with db_engine.connect() as conn:
        await conn.execute(do_ignore)
        await conn.commit()
        logger.info(f'New user {user_id} data writed')


# Get item from database
async def get_item_metadata(user_dict: dict,
                            db_engine: AsyncEngine
                            ) -> dict:
    logger.info(f'get_item_metadata({user_dict['user_id']})')

    page: int  # Current page of user from database
    result: list  # Main data of item
    user_id = user_dict['user_id']

    # Get current page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = int(row[0])
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}')

    # Getting item by index
    statement = (
        select("*")
        .select_from(catalogue)
        .where(catalogue.c.index == page)
    )

    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            result = list(row)  # row is a tuple!
            logger.info(f'Item with index {page} is executed: {result}')

    # To Dict
    item = {
        "index": result[0],
        "category": result[1],
        "name": result[2],
        "description": result[3],
        "image": result[4],
        "sell_price": result[5],
        "self_price": result[6],
        "count": result[7]
    }

    return item


# Getting users with non-user status
async def get_admins_list(db_engine: AsyncEngine) -> list:
    logger.info(f'Getting list of admins...')
    admins = []

    # Getting ID's by status
    statement = (
        select(column("telegram_id"))
        .select_from(users)
        .where(users.c.status != 'user')
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            admins.append(row[0])
            logger.info(f'{row[0]} executed as Admin')

    return admins


# Place new Order
async def new_order(db_engine: AsyncEngine,
                    i18n: TranslatorRunner,
                    user_dict: dict,
                    new_order_data: dict
                    ):
    logger.info(f'Placing new order by user {user_dict['user_id']}')

    order_counter: int  # Index of last order
    manager_id: int  # ID of manager for notification sending

    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting order counter
    order_counter_statement = (
        select(column("order_counter"))
        .select_from(variables)
    )

    async with db_engine.connect() as conn:
        raw_orders_count = await conn.execute(order_counter_statement)
        for row in raw_orders_count:
            len_orders = int(row[0])
            logger.info(f'Order counter is {len_orders}')

    # Writing statement for Orders table
    orders_statement = insert(orders).values(
        index=len_orders + 1,
        user_id=user_dict['user_id'],
        username=user_dict['username'],
        delivery_address=new_order_data['address'],
        date_and_time=date_and_time,
        item_index=new_order_data['order_metadata']['index'],
        category=new_order_data['order_metadata']['category'],
        name=new_order_data['order_metadata']['name'],
        count=new_order_data['count'],
        income=(int(new_order_data['order_metadata']['sell_price']) *
                int(new_order_data['count'])),
        pure_income=(int(new_order_data['order_metadata']['self_price']) *
                     int(new_order_data['count'])),
    )

    async with db_engine.connect() as conn:
        await conn.execute(orders_statement)
        await conn.commit()
        logger.info('New order placed')

    # Update Order Counter in Variables table
    update_order_counter = (variables.update()
                            .values(order_counter=len_orders + 1)
                            )
    # Commit to database order counter updating
    async with db_engine.connect() as conn:
        await conn.execute(update_order_counter)
        await conn.commit()
        logger.info(f'Order Counter updated to {len_orders + 1}')

    # Send notification to manager
    # Get Manager ID from Variables table
    manager_id_statement = (
        select(column("manager_id"))
        .select_from(variables)
    )

    async with db_engine.connect() as conn:
        raw_manager_id = await conn.execute(manager_id_statement)
        for row in raw_manager_id:
            manager_id = int(row[0])
            logger.info(f'Manager ID for sending notification: {manager_id}')

    # Init Bot
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.send_message(chat_id=manager_id,
                           text=i18n.order.notification(
                               index=len_orders + 1,
                               date_and_time=date_and_time,
                               user_id=user_dict['user_id'],
                               username=user_dict['username'],
                               delivery_address=new_order_data['address'],
                               name=new_order_data['order_metadata']['name'],
                               count=new_order_data['count'],
                               income=(int(new_order_data['order_metadata']['sell_price']) *
                                       int(new_order_data['count'])),
                               pure_income=(int(new_order_data['order_metadata']['self_price']) *
                                            int(new_order_data['count']))
                           )
                           )
