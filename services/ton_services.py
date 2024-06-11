import asyncio
import pprint
import json
import logging

from sqlalchemy import insert, delete, select, column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from environs import Env
from TonTools import *
from database.tables import catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

# Getting hidden consts
def _load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    logger.info(f"Enviroment executed: BOT_TOKEN, API_KEY, TEST_API_KEY, MNEMONICS")
    return [env('BOT_TOKEN'), env('API'), env('API_TEST'), env('MNEMONICS_TEST')]


COLLECTION = 'EQCDqSx4f0qz5lZ6WiGQcUoxyfs2OjltHcWhu6sfaPeg6zLT'


# Get addresses of all NFT in collection
async def get_collection(db_engine: AsyncEngine):

    logger.warning('Getting collection')

    # Init TonCenterClient MAINNET
    addresses = []
    nft_data = {}
    config = _load_config()
    client = TonCenterClient(config[1])
    logger.info('TonCenterClient started')

    # Getting all items from collection
    data = await client.get_collection(collection_address=COLLECTION)
    logger.info('Data of NFT collection is getted')
    items = await client.get_collection_items(collection=data, limit_per_one_request=1)
    logger.info('Items of NFT collection getted')

    # Writing addresses of items to Addresses list
    for item in items:
        addresses.append(item.to_dict()['address'])
        logger.info(f"Added address of item {item.to_dict()['address']}")

    # Getting NFT item by address from addresses list
    for address in addresses:
        data = await client.get_nft_items(nft_addresses=[address])

        # Writing statement for new item in database
        new_item = insert(catalogue).values(
            index=data[0].to_dict()['index'],
            name=data[0].to_dict()['metadata']['name'],
            address=data[0].to_dict()['address'],
            description=data[0].to_dict()['metadata']['description'],
            marketplace=data[0].to_dict()['metadata']['marketplace'],
            image=data[0].to_dict()['metadata']['image'],
            collection=data[0].to_dict()['collection_address'],
            owner=data[0].to_dict()['owner']
        )

        # If user already exists in database
        do_ignore = new_item.on_conflict_do_nothing(index_elements=["index"])

        # Commit to Database
        async with db_engine.connect() as conn:
            await conn.execute(do_ignore)
            await conn.commit()
            logger.info(f"NFT item {data[0].to_dict()['metadata']['name']} with address {data[0].to_dict()['address']} added to database")

    addresses.clear()
    nft_data.clear()
    logger.info('Addresses cache and NFT data cache is cleared')


async def wallet_deploy():

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
