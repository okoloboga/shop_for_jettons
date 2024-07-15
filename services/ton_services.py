import asyncio
import logging

from environs import Env
from TonTools import *

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
    return [env('BOT_TOKEN'), env('API'), env('API_TEST'), env('CENTRAL_WALLET_MNEMONICS'), 
            env('JETTON_MASTER'), env('MASTER_WALLET')]


# Init wallet for new user
async def wallet_deploy() -> list:

    logger.info('Wallet deploy')

    # Connecting to TonCenterClient
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')

    # Connect to central wallet for deploy new wallet
    central_wallet = Wallet(provider=client, mnemonics=config[3].split(), version='v4r2')
    logger.info('Central wallet activated')
    new_wallet = Wallet(provider=client)
    logger.info(f'New wallet init {new_wallet.address}')

    non_bounceable_new_wallet_address = Address(new_wallet.address).to_string(True, True, False)
    logger.info(f'New wallet unbounceable address {non_bounceable_new_wallet_address}')

    # Send some TON to new wallet
    await central_wallet.transfer_ton(destination_address=non_bounceable_new_wallet_address, 
                                      amount=0.01,
                                      message='for deploy')
    logger.info("Init TON's are sended")
    
    while True:
        new_wallet_balance = await new_wallet.get_balance()
        await asyncio.sleep(1)
        if new_wallet_balance != 0:
            logger.info(f'New wallet balance: {new_wallet_balance}')
            break
    await new_wallet.deploy()

    await asyncio.sleep(15)  # wait while transaction process

    logger.info(f'State of new wallet: {await new_wallet.get_state()}')  # active
    
    logger.info(f'New wallet is deployed {new_wallet.address}')
    
    await central_wallet.transfer_jetton(
        destination_address=new_wallet.address, 
        jetton_master_address=config[4],
        jettons_amount=15,
    )
    logger.info('Jettons transfered to new wallet')

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
    logger.info(f'jetton_wallet: {jetton_wallet}')
    await jetton_wallet.update()

    jetton_wallet_data = jetton_wallet
    logger.info(f'jetton_wallet_data after update: {jetton_wallet_data}')
    
    return int(int(jetton_wallet_data.balance) / 1000000000)


# Checking for TON value
async def ton_value(wallet: str) -> int:

    logger.info(f'TON value of wallet {wallet}')

    # Connecting to TonCenterClient TESTNET
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')

    wallet = Wallet(provider=client, address=wallet, version='v4r2')
    balance = await wallet.get_balance()
    
    logger.info(f'Wallet {wallet} have {balance / 1000000000}')

    return balance / 1000000000


# Send jettons for purchase
async def jetton_transfer(value: int,
                          costumer_mnemonics: str):
    
    logger.info(f'Send {value} jettons for purchase')

    # Connecting to TonCenterClient and central wallet
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')
    
    central_wallet = Wallet(provider=client, mnemonics=config[3].split(), version='v4r2')
    logger.info('Central wallet activated')
    costumers_wallet = Wallet(provider=client, mnemonics=costumer_mnemonics.split(), version='v4r2')
    logger.info(f'Costumers wallet activated {costumers_wallet.address}')

    await costumers_wallet.transfer_jetton(
        destination_address=central_wallet.address,
        jetton_master_address=config[4],
        jettons_amount=int(value)
    )

    logger.info(f'Jettons transfered from {costumers_wallet.address} to {config[5]}')
    
    
# Jetton transfer in game - from one player to another
async def jetton_transfer_game(value: int,
                               loser_mnemonics: str,
                               winner_wallet: str):
    
    logger.info(f'Send {value} jettons for game')

    # Connecting to TonCenterClient and central wallet
    config = _load_config()
    client = TonCenterClient(key=config[1], testnet=False)
    logger.info('TonCenterClient started')
    
    loser_wallet = Wallet(provider=client, mnemonics=loser_mnemonics.split(), version='v4r2')
    logger.info(f'Losers wallet activated {loser_wallet.address}')
    
    await loser_wallet.transfer_jetton(
        destination_address=winner_wallet,
        jetton_master_address=config[4],
        jettons_amount=int(value)
    )
    
    logger.info(f'Jettons transfered from {loser_wallet.address} to {winner_wallet}')
    
    
# To Unbouncable addres
async def to_unbouncable(wallet: str) -> str:
    return Address(wallet).to_string(True, True, False)
    



