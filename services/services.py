import json
import pprint
import random
import logging

from aiogram_dialog import DialogManager

from sqlalchemy import insert, delete, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database import users, catalogue
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
                         .values(referrals=users.c.referrals+1)
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
        page=0
    )

    # If user already exists in database
    do_ignore = new_user.on_conflict_do_nothing(index_elements=["telegram_id"])

    # Commit to Database
    async with db_engine.connect() as conn:
        await conn.execute(do_ignore)
        await conn.commit()
        logger.info(f'New user {user_id} data writed')


# Getting NFT-item from database
async def get_nft_metadata(number: int,
                           db_engine: AsyncEngine
                           ) -> dict:

    logger.info(f'get_nft_metadata({number})')
    result: list  # Main data of NFT item

    # Getting NFT by index
    statement = (
        select(column("name"), column("image"), column("description"))
        .select_from(catalogue)
        .where(catalogue.c.index == number)
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            result = list(row)  # row is tuple!
            logger.info(f'NFT item with index {number} is executed: {result}')


    # To Dict
    item = {"name": result[0],
            "image": result[1],
            "description": result[2]}

    return item

