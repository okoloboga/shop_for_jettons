import requests
import logging

from environs import Env
from config import get_config, WalletConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

privateKey = get_config(WalletConfig, "privateKey")
owner = get_config(WalletConfig, "centralWallet")
token = get_config(WalletConfig, "tokenContract")

BASE_URL = 'http://localhost:3000'


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
async def create_wallet():
    url = f'{BASE_URL}/newwallet'
    response = requests.post(url)
    return response.json()


# Get TRX balance
async def get_trx_balance(address):
    url = f'{BASE_URL}/trxbalance'
    data = {'address': address}
    response = requests.post(url, json=data)
    return response.json()


# Get Token balance
async def get_token_balance(address):
    url = f'{BASE_URL}/tokenbalance'
    params = {
        'owner': owner,
        'token': token,
        'address': address
    }
    response = requests.get(url, params=params)
    return response.json()


# Send Tron
async def send_trx(target, amount):
    url = f'{BASE_URL}/sendtrx'
    data = {
        'target': target,
        'amount': amount,
        'privateKey': privateKey
    }
    response = requests.post(url, json=data)
    return response.json()


# Send Token
async def send_token(target, amount):
    url = f'{BASE_URL}/sendtoken'
    data = {
        'owner': owner,
        'token': token,
        'target': target,
        'amount': amount,
        'privateKey': privateKey
    }
    respone = requests.post(url, json=data)
    return respone.json()

