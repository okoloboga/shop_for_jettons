import logging
import asyncio

from datetime import datetime
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from sqlalchemy import insert, select, column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from fluentogram import TranslatorRunner

from database import users, catalogue, orders, variables, stats
from config import get_config, BotConfig
from .ton_services import wallet_deploy, jetton_transfer


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


'''
newuser
'''


# New User creating after first /START pressing
async def new_user(
        db_engine: AsyncEngine,
        user_id: int,
        first_name: str,
        last_name: str,
        payload: str | None
) -> list:
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

    # New user in Stats table (for Game)
    new_stats = insert(stats).values(
        telegram_id=user_id,
        total_games=0,
        wins=0,
        loses=0,
        rate=0
        )

    # If user already exists in database
    do_ignore_user = new_user.on_conflict_do_nothing(index_elements=["telegram_id"])
    do_ignore_stats = new_stats.on_conflict_do_nothing(index_elements=["telegram_id"])

    # Commit to Database
    async with db_engine.connect() as conn:
        await conn.execute(do_ignore_user)
        await conn.execute(do_ignore_stats)
        await conn.commit()
        logger.info(f'New user {user_id} data writed')
        
    return [new_address, new_mnemonics]


# Get User data
async def get_user_account_data(user_id: int,
                                db_engine: AsyncEngine
                                ) -> dict:
    
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

    user = {
        'first_name': user_data[1],
        'last_name': user_data[2],
        'address': user_data[3],
        'purchase': user_data[5],
        'purchase_sum': user_data[6],
        'referrals': user_data[7],
    }
    
    return user

'''    
newitem
'''


# Get item from database
async def get_user_item_metadata(user_dict: dict,
                                 db_engine: AsyncEngine
                                 ) -> dict:
    logger.info(f'get_item_metadata({user_dict['user_id']})')

    page: int  # Current page of user from database
    result: list  # Main data of item
    user_id = user_dict['user_id']
    catalogue_len: int  # Number of items in catalogue

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
            
    # Get number of items in catalogue
    count = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        count_raw = await conn.execute(count)
        for row in count_raw:
            catalogue_len = row[0]
            logger.info(f'{catalogue_len} items total in Catalogue')
            
    if int(catalogue_len) != 0:

        if int(catalogue_len) <= page:
            page = 0

        async with db_engine.connect() as conn:
            for i in range(0, catalogue_len-page-1):
                result_raw = await conn.execute(select("*")
                                                .select_from(catalogue)
                                                .where(catalogue.c.index == page))
                if len(result_raw.fetchall()) == 1:
                    logger.info(f'result of page {page + i} raw with length {len(result_raw.fetchall())}: {result_raw.fetchall()}')
                    break
            for row in result_raw:
                logger.info(f'row is {row[0]}')
                result = list(row)
                logger.info(f'Item executed result is {result}')
                logger.info(f'Item with index {page + i} is executed with len {len(result_raw.fetchall())}')

                # To Dict
                item = {
                    "index": result[0],
                    "category": result[1],
                    "name": result[2],
                    "description": result[3],
                    "image": result[4],
                    "self_price": result[5],
                    "sell_price": result[6],
                    "count": result[7]
                }
                return item
    else:
        return None
    

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


'''
neworder 
'''


# Place new Order
async def new_order(db_engine: AsyncEngine,
                    i18n: TranslatorRunner,
                    user_dict: dict,
                    new_order_data: dict,
                    current_count: int
                    ) -> list:
    
    logger.info(f'Placing new order by user {user_dict['user_id']}')

    order_counter: int  # Index of last order
    manager_id: int  # ID of manager for notification sending
    costumers_mnemonics: str  # Mnemonics of TON wallet for transaction
    
    if user_dict['username'] is None:
        user_dict['username'] = 'no_username'
    
    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting order counter
    order_counter_statement = (
        select(column("orders_counter"))
        .select_from(variables)
    )

    async with db_engine.connect() as conn:
        raw_orders_count = await conn.execute(order_counter_statement)
        for row in raw_orders_count:
            len_orders = int(row[0])
            logger.info(f'Order counter is {len_orders}')
            
    income = int(new_order_data['order_metadata']['sell_price']) * int(new_order_data['count'])
    pure_income = income - int(new_order_data['order_metadata']['self_price']) * int(new_order_data['count'])

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
        income=income,
        pure_income=pure_income,
        status='new'
    )

    # If user already exists in database
    do_ignore_order = orders_statement.on_conflict_do_nothing(index_elements=["index"])

    async with db_engine.connect() as conn:
        await conn.execute(do_ignore_order)
        await conn.commit()
        logger.info('New order placed')

    # Update Order Counter in Variables table
    update_orders_counter = (variables.update()
                            .values(orders_counter=len_orders + 1)
                            )
    
    # Update count of Items in catralogue
    update_catalogue_counter = (catalogue.update()
                                .values(count=(current_count - int(new_order_data['count'])))
                                .where(catalogue.c.index == new_order_data['order_metadata']['index'])
                                )
    
    
    # Commit to database order counter updating
    async with db_engine.connect() as conn:
        await conn.execute(update_orders_counter)
        await conn.execute(update_catalogue_counter)
        await conn.commit()
        logger.info(f'Orders Counter updated to {len_orders + 1},\
            Catalogue count update by {new_order_data['count']}')

    # Send notification to manager and getting Mnemonics of costumer
    # Get Manager ID from Variables table
    manager_id_statement = (
        select(column("manager_id"))
        .select_from(variables)
    )
    # Get costumers mnemonics from Users table
    costumers_mnemonics_statement = (
        select(column("mnemonics"))
        .select_from(users)
        .where(users.c.telegram_id == user_dict['user_id'])
    )
    async with db_engine.connect() as conn:
        raw_manager_id = await conn.execute(manager_id_statement)
        raw_costumers_mnemonics = await conn.execute(costumers_mnemonics_statement)
        for row in raw_manager_id:
            manager_id = int(row[0])
            logger.info(f'Manager ID for sending notification: {manager_id}')
        for row in raw_costumers_mnemonics:
            costumers_mnemonics = row[0]
            logger.info(f'Costumers Mnemonics are executed')
            
    # SEND JETTONS FOR PURCHASE
    await jetton_transfer(value=int(new_order_data['order_metadata']['sell_price']) *
                                int(new_order_data['count']),
                          costumer_mnemonics=costumers_mnemonics)
    

    # Init Bot for sending notification to manager
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Send notification to manager
    await bot.send_message(chat_id=manager_id,
                           text=i18n.order.notification(
                               index=len_orders + 1,
                               date_and_time=date_and_time,
                               user_id=user_dict['user_id'],
                               username=user_dict['username'],
                               delivery_address=new_order_data['address'],
                               name=new_order_data['order_metadata']['name'],
                               count=new_order_data['count'],
                               income=income,
                               pure_income=pure_income
                               )
                           )

    return [len_orders + 1, date_and_time]


# Check for #admin_panel command
def is_admin(text: str) -> str:
    logger.info(f'is_admin({text})')
    if text == '#admin_panel':
        return text
    raise ValueError

