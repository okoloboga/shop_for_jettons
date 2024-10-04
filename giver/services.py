import logging
import datetime

from sqlalchemy import select, column, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from database import users


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Create new User
async def create_new_user(user_id: int,
                          first_name: str,
                          last_name: str,
                          db_engine: AsyncEngine,
                          addresses: dict):
    
    eth_address = addresses['eth_address']
    sol_address = addresses['sol_address']

    statement = (
        insert(users)
        .values(telegram_id=user_id,
                first_name=first_name, 
                last_name=last_name, 
                eth_address=eth_address, 
                sol_address=sol_address,
                last_get="2000-01-01 00:00:00")
    )
    do_ignore_user = statement.on_conflict_do_nothing(index_elements=["telegram_id"])
    async with db_engine.connect() as conn:
        await conn.execute(do_ignore_user)
        await conn.commit()


# Get User data
async def get_user_data(user_id: int,
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
        'eth_address': user_data[3],
        'sol_address': user_data[4],
        'last_get': user_data[5]
    }
    
    return user


# Check Users Last Get
async def check_last_get(user_id: int,
                         db_engine: AsyncEngine
                         ) -> dict:
    
    # Read users data from database
    statement = (
        select(column('last_get'))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )
    async with db_engine.connect() as conn:
        user_data_raw = await conn.execute(statement)
        for row in user_data_raw:
            user_data = list(row)
            logger.info(f'Statement\n{user_data}\nexecuted of user {user_id}')

    last_get = user_data[0]
    now = datetime.datetime.now()
    one_week_ago = now - datetime.timedelta(days=7)

    return last_get < one_week_ago


# Update ETH Address in database
async def update_eth_address(user_id: int,
                             eth_address: str,
                             db_engine: AsyncEngine
                             ):
    statement = (
        update(users)
        .where(users.c.telegram_id == user_id)
        .values(eth_address=eth_address)
    )
    async with db_engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()

    
# Update SOL Address in database
async def update_sol_address(user_id: int,
                             sol_address: str,
                             db_engine: AsyncEngine
                             ):
    statement = (
        update(users)
        .where(users.c.telegram_id == user_id)
        .values(sol_address=sol_address)
    )
    async with db_engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()
