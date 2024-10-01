import requests
import logging

from environs import Env
from config import get_config, WalletConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

wallet = get_config(WalletConfig, "wallet")

BASE_URL = 'http://localhost:3000/api'


'''
# Get Ethereum balance
async def get_eth_balance(address):
    url = f'{BASE_URL}/ethbalance'
    params = {'address': address}
    response = requests.get(url, params=params)
    return response.json()


# Send Ethereum
async def send_eth(sender, privateKey, target, amount):
    url = f'{BASE_URL}/sendeth'
    data = {
        'sender': sender,
        'privateKey': privateKey,
        'target': target,
        'amount': amount
    }
    response = requests.post(url, json=data)
    return response.json()


# Get Solana Balance
async def get_sol_balance(address):
    url = f'{BASE_URL}/solbalance'
    params = {'address': address}
    response = requests.get(url, params=params)
    return response.json()


# Send Solana
async def send_sol(target, amount, privateKey):
    url = f'{BASE_URL}/sendsol'
    data = {
        'target': target,
        'amount': amount,
        'privateKey': privateKey
    }
    response = requests.post(url, json=data)
    return response.json()


# Get Fantom balance
async def get_ftm_balance(address):
    url = f'{BASE_URL}/ftmbalance'
    params = {'address': address}
    response = requests.get(url, params=params)
    return response.json()


# Send Fantom
async def send_ftm(sender, target, amount, privateKey):
    url = f'{BASE_URL}/sendftm'
    data = {
        'sender': sender,
        'target': target,
        'amount': amount,
        'privateKey': privateKey
    }
    response = requests.post(url, json=data)
    return response.json()
'''


# Create TRX wallet
async def create_wallet() -> dict:
    url = f'{BASE_URL}/newwallet'
    response = requests.post(url)
    return response.json()


# Get TRX balance
async def get_trx_balance(address: str
                          ) -> dict:

    url = f'{BASE_URL}/trxbalance?address={address}'

    logger.info(f'Get TRX balance: {address}')

    response = requests.get(url)

    logger.info(f'Get TRX balance: {response.json()}')

    return response.json()


# Get Token balance
async def get_token_balance(address: str
                            ) -> dict:

    url = f'{BASE_URL}/tokenbalance?owner={wallet.centralWallet}&token={wallet.tokenContract}&address={address}'

    logger.info(f'Get Token balance: {address}')

    response = requests.get(url)
    
    logger.info(f'Get Token balance: {response.json()}')
    
    return response.json()


# Send Tron
async def send_trx(target: str, 
                   amount: str | float
                   ) -> dict:

    url = f'{BASE_URL}/trxtransaction?target={target}&amount={amount}&privateKey={wallet.privateKey}'

    logger.info(f'Send TRX: {target} amount: {amount}')

    response = requests.post(url)

    logger.info(f'Send TRX: {response.json()}')

    return response.json()


# Send Token
async def send_token(owner: str, 
                     private_key: str, 
                     target: str, 
                     amount: str | float
                     ) -> dict:

    url = f'{BASE_URL}/tokentransaction?owner={owner}&token={wallet.tokenContract}&target={target}&amount={amount}&privateKey={private_key}'

    logger.info(f'Send Token: {target} amount: {amount}')

    respone = requests.post(url)

    logger.info(f'Send Token: {respone.json()}')

    return respone.json()

