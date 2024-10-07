import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input.text import ManagedTextInput
from fluentogram import TranslatorRunner
from sqlalchemy import select, column
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from states import MainSG
from database import users
from services import *
from config import get_config, WalletConfig
from request import *


router = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Process START command
@router.message(CommandStart())
async def command_start_process(message: Message,
                                db_engine: AsyncEngine,
                                dialog_manager: DialogManager,
                                command: CommandObject):
    
    user_id = message.from_user.id
    user: list = []  # Prepare for user data

    logger.info(f'Command START by user {user_id}')
    
    # Read users data from database
    statement = (
        select(column('first_name'))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    async with db_engine.connect() as conn:
        user_data = await conn.execute(statement)
        for row in user_data:
            user.append(row[0])
            logger.info(f'User {message.from_user.id} data is loaded.\
                        \nusers first name: {user}')

    logger.info(f'User data: {user}')

    # If user is new - offer to fill ETH address
    if len(user) == 0:
        await dialog_manager.start(MainSG.fill_eth, 
                                   mode=StartMode.RESET_STACK)
        logger.info(f'User {user} is new')
    else:
        await dialog_manager.start(MainSG.select_coin, 
                                   mode=StartMode.RESET_STACK)
        logger.info(f'User {user} is old')


# Check ETH address
async def check_eth_address(message: Message,
                            widget: ManagedTextInput,
                            dialog_manager: DialogManager,
                            address: str):

    user = message.from_user.id

    logger.info(f'Check ETH address: {user} {address}')

    response = await eth_address(address)

    logger.info(f'Check ETH address: {response}')
    
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')

    if response['data'] != False and response['status'] == 'OK':
        await state.update_data(eth_address=address)
        await dialog_manager.switch_to(MainSG.fill_trx)
    else:
        await message.answer(text=i18n.error.ethaddress())

    
# Check ETH address
async def check_trx_address(message: Message,
                            widget: ManagedTextInput,
                            dialog_manager: DialogManager,
                            address: str):

    user = message.from_user.id

    logger.info(f'Check TRX address: {user} {address}')

    response = await get_trx_balance(address)

    logger.info(f'Check TRX address: {response}')
    
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    if response['data'] != False and response['status'] == 'OK':
        await state.update_data(trx_address=address)
        adresses = await state.get_data()
        
        # Write new user to database
        await create_new_user(user_id, 
                              first_name, 
                              last_name, 
                              db_engine,
                              adresses)

        logger.info(f'User {user_id} is created')

        await dialog_manager.switch_to(MainSG.select_coin)
    else:
        await message.answer(text=i18n.error.trxaddress())

'''
# Check SOL address
async def check_sol_address(message: Message,
                            widget: ManagedTextInput,
                            dialog_manager: DialogManager,
                            address: str):

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f'Check SOL address: {user_id} {address}')

    response = await sol_address(address)

    logger.info(f'Check SOL address: {response}')
    
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    if response['data'] != False and response['status'] == 'OK':
        await state.update_data(sol_address=address)
        adresses = await state.get_data()
        
        # Write new user to database
        await create_new_user(user_id, 
                              first_name, 
                              last_name, 
                              db_engine,
                              adresses)

        logger.info(f'User {user_id} is created')

        await dialog_manager.switch_to(MainSG.select_coin)
    else:
        await message.answer(text=i18n.error.soladdress())
'''


# Send ETH
async def select_eth(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    logger.info(f'Select ETH: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_data(user, db_engine))['eth_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = float((await get_eth_balance(central_wallet.ethAddress))['data'])
        
        logger.info(f'Central balance: {central_balance}')

        if (central_balance - 0.01) > central_wallet.ethQuote:
            result = await send_eth(central_wallet.ethAddress, 
                                    central_wallet.ethPrivateKey,
                                    user_wallet,
                                    central_wallet.ethQuote)

            logger.info(f'Send ETH: {result}')

            if result['status'] == 'OK':
                await update_last_get(user, db_engine)
                await callback.message.answer(text=i18n.success.eth(hash=result['data']))
            else:
                await callback.message.answer(text=i18n.error.send())
        else:
            await callback.message.answer(text=i18n.error.central.balance())
    else:
        await callback.message.answer(text=i18n.error.lastget())


# Send FTM
async def select_ftm(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    logger.info(f'Select FTM: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_data(user, db_engine))['eth_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = float((await get_ftm_balance(central_wallet.ethAddress))['data'])
        
        logger.info(f'Central balance: {central_balance}')

        if (central_balance - 0.0001) > central_wallet.ftmQuote:
            result = await send_ftm(central_wallet.ethAddress, 
                                    user_wallet,
                                    central_wallet.ftmQuote,
                                    central_wallet.ethPrivateKey)

            logger.info(f'Send FTM: {result}')

            if result['status'] == 'OK':
                await update_last_get(user, db_engine)
                await callback.message.answer(text=i18n.success.ftm(hash=result['data']))
            else:
                await callback.message.answer(text=i18n.error.send())
        else:
            await callback.message.answer(text=i18n.error.central.balance())
    else:
        await callback.message.answer(text=i18n.error.lastget())

'''
# Send SOL
async def select_sol(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    logger.info(f'Select SOL: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_data(user, db_engine))['sol_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = float((await get_sol_balance(central_wallet.solAddress))['data'])
        
        logger.info(f'Central balance: {central_balance}')

        if (central_balance - 0.0001) > central_wallet.solQuote:
            result = await send_sol(user_wallet,
                                    central_wallet.solQuote,
                                    central_wallet.solPrivateKey)

            logger.info(f'Send SOL: {result}')

            if result['status'] == 'OK':
                await update_last_get(user, db_engine)
                await callback.message.answer(text=i18n.success.sol(hash=result['data']))
            else:
                await callback.message.answer(text=i18n.error.send())
        else:
            await callback.message.answer(text=i18n.error.central.balance())
    else:
        await callback.message.answer(text=i18n.error.lastget())
'''


# Send TRX
async def select_trx(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    logger.info(f'Select TRX: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_data(user, db_engine))['trx_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = float((await get_trx_balance(central_wallet.trxAddress))['data'])
        
        logger.info(f'Central balance: {central_balance}')

        if (central_balance - 0.0001) > central_wallet.trxQuote:
            result = await send_trx(user_wallet,
                                    central_wallet.trxQuote,
                                    central_wallet.trxPrivateKey)

            logger.info(f'Send TRX: {result}')

            if result['status'] == 'OK':
                await update_last_get(user, db_engine)
                await callback.message.answer(text=i18n.success.trx(hash=result['data']))
            else:
                await callback.message.answer(text=i18n.error.send())
        else:
            await callback.message.answer(text=i18n.error.central.balance())
    else:
        await callback.message.answer(text=i18n.error.lastget())

# Go to Account menu
async def account(callback: CallbackQuery,
                  button: Button,
                  dialog_manager: DialogManager):

    user = callback.from_user.id
    logger.info(f'Account menu: {user}')

    await dialog_manager.switch_to(MainSG.account)


# Check new address
async def check_address(message: Message,
                        widget: ManagedTextInput,
                        dialog_manager: DialogManager,
                        address: str):

    user = message.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('db_engine')

    logger.info(f'Check address: {user} {address}')

    if address[0:3] == 'ETH':
        response = await eth_address(address[4:])

        logger.info(f'Check ETH address: {response}')

        if response['data'] != False:
            await update_eth_address(user, address[4:], db_engine)
        else:
            await message.answer(text=i18n.error.ethaddress())
    
    # elif address[0:3] == 'SOL':
    #     response = await sol_address(address[4:])
    # 
    #     logger.info(f'Check SOL address: {response}')
    # 
    #     if response['data'] != False:
    #         await update_sol_address(user, address[4:], db_engine)
    #     else:
    #         await message.answer(text=i18n.error.soladdress())

    elif address[0:3] == 'TRX': 
        response = await get_trx_balance(address[4:])

        logger.info(f'Check TRX address: {response}')

        if response['data'] != False:
            await update_trx_address(user, address[4:], db_engine)
        else:
            await message.answer(text=i18n.error.trxaddress())
    else:
        await message.answer(text=i18n.error.address())


# Process BACK button
async def back(callback: CallbackQuery,
               button: Button,
               dialog_manager: DialogManager):

    user = callback.from_user.id
    logger.info(f'Back: {user}')

    await dialog_manager.switch_to(MainSG.select_coin)


async def wrong_input(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      address: str):

    logger.info(f'User {callback.from_user.id} fills wrong message')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    await callback.answer(text=i18n.wrong.input())
