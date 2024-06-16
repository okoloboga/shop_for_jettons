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
    logger.info("Enviroment executed")
    return [env('BOT_TOKEN'), env('API'), env('API_TEST'), env('CENTRAL_WALLET_MNEMONICS'), env('JETTON_MASTER')]


# Init wallet for new user
async def wallet_deploy() -> list:

    logger.info('Wallet deploy')

    # Connecting to TonCenterClient TESTNET
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')

    # Connect to central wallet for deploy new wallet
    my_wallet = Wallet(provider=client, mnemonics=config[3].split(), version='v4r2')
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


# Jettons value in wallet
async def jetton_value(wallet: str) -> int:

    logger.info(f'Jetton value of wallet {wallet}')

    # Connecting to TonCenterClient TESTNET
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')

    # Get jetton wallet
    jetton_wallet = await (Jetton(config[4], client)
                           .get_jetton_wallet(owner_address=wallet))
    await jetton_wallet.update()

    jetton_wallet_data = jetton_wallet

    return int(int(jetton_wallet_data.balance) / 1000000000)