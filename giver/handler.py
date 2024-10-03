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
from services import create_new_user, check_last_get
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
    
    user = message.from_user.id

    logger.info(f'Command START by user {user}')
    
    # Read users data from database
    statement = (
        select(column('first_name'))
        .select_from(users)
        .where(users.c.telegram_id == message.from_user.id)
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

    response = await check_eth_address(address)

    logger.info(f'Check ETH address: {response}')
    
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')

    if response['status'] == 'OK':
        await state.update_data(eth_address=address)
        await dialog_manager.switch_to(MainSG.fill_sol)
    else:
        await message.answer(text=i18n.error.eth_address())


# Check SOL address
async def check_sol_address(message: Message,
                            widget: ManagedTextInput,
                            dialog_manager: DialogManager,
                            address: str):

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    logger.info(f'Check SOL address: {user_id} {address}')

    response = await check_sol_address(address)

    logger.info(f'Check SOL address: {response}')
    
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    state: FSMContext = dialog_manager.middleware_data.get('state')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('session')

    if response['status'] == 'OK':
        await state.update_data(sol_address=address)
        adresses = await state.get_data()
        
        # Write new user to database
        await create_new_user(user_id, 
                              first_name, 
                              last_name, 
                              db_engine,
                              adresses)

        logger.info(f'User {user_id} is created')

        await dialog_manager.switch_to(MainSG.coin_getter)
    else:
        await message.answer(text=i18n.error.sol_address())


# Send ETH
async def select_eth(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('session')

    logger.info(f'Select ETH: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_account_data(user, db_engine))['eth_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = await get_eth_balance(central_wallet.ethAddress)
        
        logger.info(f'Central balance: {central_balance}')

        if central_balance > central_wallet.ethQuote:
            result = await send_eth(central_wallet.ethAddress, 
                                    central_wallet.ethPrivateKey,
                                    user_wallet,
                                    central_wallet.ethQuote)

            logger.info(f'Send ETH: {result}')

            await callback.message.answer(text=i18n.success.eth())
        else:
            await callback.message.answer(text=i18n.error.central_balance())
    else:
        await callback.message.answer(text=i18n.error.last_get())


# Send FTM
async def select_ftm(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('session')

    logger.info(f'Select FTM: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_account_data(user, db_engine))['eth_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = await get_ftm_balance(central_wallet.ethAddress)
        
        logger.info(f'Central balance: {central_balance}')

        if central_balance > central_wallet.ftmQuote:
            result = await send_ftm(central_wallet.ethAddress, 
                                    central_wallet.ethPrivateKey,
                                    user_wallet,
                                    central_wallet.ftmQuote)

            logger.info(f'Send FTM: {result}')

            await callback.message.answer(text=i18n.success.ftm())
        else:
            await callable.message.answer(text=i18n.error.central_balance())
    else:
        await callback.message.answer(text=i18n.error.last_get())


# Send SOL
async def select_sol(callback: CallbackQuery,
                     button: Button,
                     dialog_manager: DialogManager):

    user = callback.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('session')

    logger.info(f'Select SOL: {user}')

    time = await check_last_get(user, db_engine)

    if time == True:
        user_wallet = (await get_user_account_data(user, db_engine))['sol_address']
        central_wallet = get_config(WalletConfig, 'wallet')
        central_balance = await get_sol_balance(central_wallet.solAddress)
        
        logger.info(f'Central balance: {central_balance}')

        if central_balance > central_wallet.solQuote:
            result = await send_sol(central_wallet.solAddress, 
                                    central_wallet.solPrivateKey,
                                    user_wallet,
                                    central_wallet.solQuote)

            logger.info(f'Send SOL: {result}')

            await callback.message.answer(text=i18n.success.sol())
        else:
            await callback.message.answer(text=i18n.error.central_balance())
    else:
        await callback.message.answer(text=i18n.error.last_get())


# Go to Account menu
async def account(callback: CallbackQuery,
                  button: Button,
                  dialog_manager: DialogManager):

    user = callback.from_user.id
    logger.info(f'Account menu: {user}')

    await dialog_manager.switch_to(MainSG.account)


# Check new address
async def check_address(message: Message,
                        widget: ManagedTextInput,
                        dialog_manager: DialogManager,
                        address: str):

    user = message.from_user.id
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    db_engine: AsyncEngine = dialog_manager.middleware_data.get('session')

    logger.info(f'Check address: {user} {address}')

    if address[0:3] == 'ETH':
        response = await check_eth_address(address)

        logger.info(f'Check ETH address: {response}')

        if response['result'] == 'OK':
            await update_eth_address(user, address[4:], db_engine)
        else:
            await message.answer(text=i18n.error.eth_address())

    elif address[0:3] == 'SOL':
        response = await check_sol_address(address)

        logger.info(f'Check SOL address: {response}')

        if response['result'] == 'OK':
            await update_sol_address(user, address[4:], db_engine)
        else:
            await message.answer(text=i18n.error.sol_address())
    else:
        await message.answer(text=i18n.error.address())


# Process BACK button
async def back(callback: CallbackQuery,
               button: Button,
               dialog_manager: DialogManager):

    user = callback.from_user.id
    logger.info(f'Back: {user}')

    await dialog_manager.switch_to(MainSG.main)


async def wrong_input(callback: CallbackQuery,
                      widget: ManagedTextInput,
                      dialog_manager: DialogManager,
                      address: str):

    logger.info(f'User {callback.from_user.id} fills wrong message')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    await callback.answer(text=i18n.wrong.input())
