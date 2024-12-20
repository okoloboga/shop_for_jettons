import logging
import asyncio

from datetime import datetime
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from sqlalchemy import select, column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from fluentogram import TranslatorRunner

from database import users, catalogue, orders, variables, stats
from config import get_config, WalletConfig
from .requests import create_trx_wallet, send_token, send_trx


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


'''
newuser
'''


# New User creating after first /START pressing
async def new_user(db_engine: AsyncEngine,
                   user_id: int,
                   first_name: str,
                   last_name: str,
                   payload: str | None
                   ) -> list:

    logger.info('new_user processing')

    # Create new wallet and send init Tron
    central_wallet = get_config(WalletConfig, 'wallet')
    new_wallet = await create_trx_wallet()

    logger.info(f'New wallet: {new_wallet}, lets send 0.1 TRON and 15 tokens to new wallet address:\n\
        {new_wallet["data"]["address"]["base58"]}')

    # Get address and private key of new wallet and transfer 15 start coins there
    new_address = new_wallet['data']['address']['base58']
    new_private_key = new_wallet['data']['privateKey']
    send_trx_result = await send_trx(new_address, 0.1)
    send_token_result = await send_token(central_wallet.centralWallet,
                                         central_wallet.privateKey, 
                                         new_address, 
                                         15)

    logger.info(f'send TRX result: {send_trx_result['status']}\nsend token result: {send_token_result["status"]}')

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
        private_key=new_private_key,
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
        
    return [new_address, new_private_key]


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
            result_raw = await conn.execute(select("*")
                                            .select_from(catalogue)
                                            .where(catalogue.c.index == page))
            for row in result_raw:
                logger.info(f'row is {row[0]}')
                result = list(row)
                logger.info(f'Item executed result is {result}')

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
                    bot: Bot,
                    user_dict: dict,
                    new_order_data: dict,
                    current_count: int
                    ) -> list:
    
    logger.info(f'Placing new order by user {user_dict['user_id']}')

    manager_id: int  # ID of manager for notification sending
    costumers_private_key: str  # Private Key of Tron wallet for transaction
    
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
    
    # Prices in $
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

    # Send notification to manager and getting Private Key of costumer
    # Get Manager ID from Variables table
    manager_id_statement = (
        select(column("manager_id"))
        .select_from(variables)
    )
    # Get costumers Private key from Users table
    costumers_private_key_statement = (
        select(column("private_key"))
        .select_from(users)
        .where(users.c.telegram_id == user_dict['user_id'])
    )
    # Get costumers address from Users table
    costumers_wallet_statement = (
        select(column("address"))
        .select_from(users)
        .where(users.c.telegram_id == user_dict['user_id'])
    )

    async with db_engine.connect() as conn:
        raw_manager_id = await conn.execute(manager_id_statement)
        raw_costumers_private_key = await conn.execute(costumers_private_key_statement)
        raw_costumers_wallet = await conn.execute(costumers_wallet_statement)
        for row in raw_manager_id:
            manager_id = int(row[0])
            logger.info(f'Manager ID for sending notification: {manager_id}')
        for row in raw_costumers_private_key:
            costumers_private_key = row[0]
            logger.info(f'Costumers private key are executed: {costumers_private_key}')
        for row in raw_costumers_wallet:
            costumers_wallet = row[0]
            logger.info(f'Costumers wallet are executed: {costumers_wallet}')
    
    # Central wallet for sending tokens
    central_wallet = get_config(WalletConfig, 'wallet')
    token_price = await get_token_price(db_engine)
    
    # SEND TOKENS FOR PURCHASE
    await send_token(owner=central_wallet.centralWallet,
                     private_key=costumers_private_key,
                     target=central_wallet.centralWallet,
                     amount=int(new_order_data['order_metadata']['sell_price']) *
                           int(new_order_data['count']) * token_price,
                     )

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
                               income_in_tokens=income * token_price,
                               pure_income_in_tokens=pure_income * token_price,
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


# Get token price
async def get_token_price(db_engine: AsyncEngine) -> float:
    token_price_statement = (
        select(column("token_price"))
        .select_from(variables) 
    )
    async with db_engine.connect() as conn:
        raw_token_price = await conn.execute(token_price_statement)
        for row in raw_token_price:
            token_price = float(row[0])
            logger.info(f'Token price: {token_price}')
            return token_price

