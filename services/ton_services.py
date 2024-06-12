import asyncio
import pprint
import json
import logging

from sqlalchemy import insert, delete, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from environs import Env
from TonTools import *

from database import catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Getting hidden consts
def _load_config(path: str | None = None) -> list:
    env = Env()
    env.read_env(path)
    logger.info(f"Enviroment executed: BOT_TOKEN, API_KEY, TEST_API_KEY, MNEMONICS")
    return [env('BOT_TOKEN'), env('API'), env('API_TEST'), env('MNEMONICS_TEST')]


async def wallet_deploy() -> list:

    logger.info('Wallet deploy')

    # Connecting to TonCenterClient TESTNET
    config = _load_config()
    client = TonCenterClient(key=config[-2], testnet=True)
    logger.info('TonCenterClient started')

    # Connect to ctntral wallet for deploy new wallet
    my_wallet = Wallet(provider=client, mnemonics=config[-1].split(), version='v4r2')
    logger.info('Central wallet activated')
    new_wallet = Wallet(provider=client)
    logger.info('New wallet init')

    non_bounceable_new_wallet_address = Address(new_wallet.address).to_string(True,
                                                                              True,
                                                                              False)
    logger.info(f'New wallet unbounceable address {non_bounceable_new_wallet_address}')

    # Send some TON to new wallet
    await my_wallet.transfer_ton(destination_address=non_bounceable_new_wallet_address, amount=0.02,
                                 message='for deploy')
    logger.info("Init TON's are sended")
    await new_wallet.deploy()
    logger.info('New wallet is deployed')

    return [new_wallet.address, new_wallet.mnemonics]
