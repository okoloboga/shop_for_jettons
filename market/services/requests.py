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

BASE_URL = 'http://backend:3000/api'


# Create TRX wallet
async def create_trx_wallet() -> dict:
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


# ### #
# TON #
# ### #


# Create TON wallet
async def create_ton_wallet() -> dict:

    url = f'{BASE_URL}/newTonWallet'

    logger.info('Creating a new TON wallet')

    response = requests.get(url)

    logger.info(f'Server response: {response.json()}')

    return response.json()


# Get TON balance
async def get_ton_balance(wallet_address: str
                          ) -> dict:

    url = f'{BASE_URL}/getTonBalance?walletAddress={wallet_address}'

    logger.info(f'Getting TON balance for address: {wallet_address}')
    
    response = requests.get(url)
    
    logger.info(f'Server response: {response.json()}')
    
    return response.json()


# Get Jetton balance
async def get_jetton_balance(wallet_address: str, 
                             jetton_address: str
                             ) -> dict:

    url = f'{BASE_URL}/getJettonBalance?walletAddress={wallet_address}&jettonAddress={jetton_address}'
    
    logger.info(f'Getting Jetton balance for address: {wallet_address}, Jetton: {jetton_address}')
    
    response = requests.get(url)
    
    logger.info(f'Server response: {response.json()}')
    
    return response.json()


# Send TON transaction
async def send_ton_transaction(to_address: str, 
                               amount: str, 
                               private_key: str
                               ) -> dict:

    url = f'{BASE_URL}/sendTonTransaction?toAddress={to_address}&amount={amount}&privateKey={private_key}'
    
    logger.info(f'Sending TON transaction to {to_address}, amount: {amount}')
    
    response = requests.post(url)
    
    logger.info(f'Server response: {response.json()}')
    
    return response.json()


# Send Jetton transaction
async def send_jetton_transaction(to_address: str, 
                                  jetton_address: str, 
                                  amount: str, 
                                  private_key: str
                                  ) -> dict:

    url = f'{BASE_URL}/sendJettonTransaction?toAddress={to_address}&jettonAddress={jetton_address}&amount={amount}&privateKey={private_key}'
    
    logger.info(f'Sending Jetton transaction to {to_address}, amount: {amount}, Jetton: {jetton_address}')
    
    response = requests.post(url)
    
    logger.info(f'Server response: {response.json()}')
    
    return response.json()
