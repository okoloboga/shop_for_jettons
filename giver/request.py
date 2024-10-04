import requests
import logging

from config import get_config, WalletConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')

wallet = get_config(WalletConfig, "wallet")

BASE_URL = 'http://backend:3000/api'


# Get Ethereum balance
async def get_eth_balance(address: str
                         ) -> dict:

    url = f'{BASE_URL}/ethbalance?address={address}'

    logger.info(f'Get ETH balance: {address}')

    response = requests.get(url)

    logger.info(f'Get ETH balance: {response.json()}')

    return response.json()


# Check Ethereum address
async def eth_address(address: str
                      ) -> dict:

    url = f'{BASE_URL}/ethaddress?address={address}'

    logger.info(f'Check ETH address: {address}')

    response = requests.get(url)

    logger.info(f'Check ETH address: {response.json()}')

    return response.json()


# Check Solana address
async def sol_address(address: str
                      ) -> dict:

    url = f'{BASE_URL}/soladdress?address={address}'

    logger.info(f'Check Solana address: {address}')

    response = requests.get(url)

    logger.info(f'Check Solana address: {response.json()}')

    return response.json()


# Send Ethereum
async def send_eth(sender: str, 
                   privateKey: str, 
                   target: str, 
                   amount: str | float
                   ) -> dict:

    url = f'{BASE_URL}/ethtransaction?sender={sender}&privateKey={privateKey}&target={target}&amount={amount}'
    
    logger.info(f'Send ETH: sender: {sender} target: {target} amount: {amount}')

    response = requests.post(url)

    logger.info(f'Send ETH: {response.json()}')

    return response.json()


# Get Solana Balance
async def get_sol_balance(address: str
                         ) -> dict:
    
    url = f'{BASE_URL}/solbalance?address={address}'

    logger.info(f'Get SOL balance: {address}')

    response = requests.get(url)

    logger.info(f'Get SOL balance: {response.json()}')

    return response.json()


# Send Solana
async def send_sol(target: str, 
                   amount: str | float, 
                   privateKey: str
                   ) -> dict:

    url = f'{BASE_URL}/soltransaction?target={target}&amount={amount}&privateKey={privateKey}'
    
    logger.info(f'Send SOL: target: {target} amount: {amount}')

    response = requests.post(url)

    logger.info(f'Send SOL: {response.json()}')

    return response.json()


# Get Fantom balance
async def get_ftm_balance(address: str
                         ) -> dict:

    url = f'{BASE_URL}/ftmbalance?address={address}'

    logger.info(f'Get Fantom balance: {address}')

    response = requests.get(url)

    logger.info(f'Get Fantom balance: {response.json()}')

    return response.json()


# Send Fantom
async def send_ftm(sender: str, 
                   target: str, 
                   amount: str | float, 
                   privateKey: str
                   ) -> dict:

    url = f'{BASE_URL}/ftmtransaction?sender={sender}&target={target}&amount={amount}&privateKey={privateKey}'
    
    logger.info(f'Send Fantom: sender: {sender} target: {target} amount: {amount}')

    response = requests.post(url)

    logger.info(f'Send Fantom: {response.json()}')

    return response.json()
