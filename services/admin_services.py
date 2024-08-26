import logging
import validators

from datetime import datetime
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from sqlalchemy import insert, delete, select, column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from fluentogram import TranslatorRunner

from database import *
from config import get_config, BotConfig

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Get user from database
async def get_user_data(user_id: int,
                        db_engine: AsyncEngine
                        ) -> dict:
    logger.info(f'get_user_data({user_id})')
    result_list: list  # Main data of user in list
    result: dict  # Result dict for return
    
    # Read users data from database
    statement = (
        select("*")
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )
    async with db_engine.connect() as conn:
        user_data_raw = await conn.execute(statement)
        for row in user_data_raw:
            user_data = list(row)
        logger.info(f'Statement\n{user_data}\nexecuted of user {user_id}')

    result = {
        'telegram_id': user_data[0],
        'first_name': user_data[1],
        'last_name': user_data[2],
        'address': user_data[3],
        'mnemonics': user_data[4],
        'purchase': user_data[5],
        'purchase_sum': user_data[6],
        'referrals': user_data[7],
        'invited': user_data[8],
        'page': user_data[9],
        'status': user_data[10]        
    }
    
    return result
    
# Get item from database
async def get_admin_item_metadata(number: int,
                            db_engine: AsyncEngine
                            ) -> dict:
    logger.info(f'get_item_metadata({number})')
    result: list  # Main data of item

    # Getting item by index
    statement = (
        select(column("category"), column("name"), column("description"),
               column("image"), column("sell_price"), column("self_price"),
               column("count"))
        .select_from(catalogue)
        .where(catalogue.c.index == number)
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            result = list(row)  # row is tuple!
            logger.info(f'Item with index {number} is executed: {result}')

    # To Dict
    item = {
            "category": result[0],
            "name": result[1],
            "description": result[2],
            "image": result[3],
            "sell_price": result[4],
            "self_price": result[5],
            "count": result[6]
    }

    return item


# Getting users with non-user status
async def get_admins_list(db_engine: AsyncEngine) -> list:
    logger.info(f'Getting list of admins...')
    admins = []

    # Getting ID's by status
    statement = (
        select(column("telegram_id"))
        .select_from(users)
        .where(users.c.status != 'user')
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            admins.append(row[0])
            logger.info(f'{row[0]} executed as Admin')

    return admins


# Checking for URL
def check_url(url: str) -> str:
    if validators.url(url):
        return url
    raise ValueError


# Checking Sell price, Self price and count
def check_price_count(text: str) -> str:
    text_list = text.split()
    if len(text_list) == 3:
        for i in text_list:
            if not i.isdigit():
                raise ValueError
        else:
            return text
    raise ValueError


# Checking len of description string in new item and item edit
def len_check(text: str) -> str:
    if len(text) <= 624:
        return text
    raise ValueError

'''
                                   __    __                             
                                  |  \  |  \                            
 _______    ______   __   __   __  \$$ _| $$_     ______   ______ ____  
|       \  /      \ |  \ |  \ |  \|  \|   $$ \   /      \ |      \    \ 
| $$$$$$$\|  $$$$$$\| $$ | $$ | $$| $$ \$$$$$$  |  $$$$$$\| $$$$$$\$$$$
| $$  | $$| $$    $$| $$ | $$ | $$| $$  | $$ __ | $$    $$| $$ | $$ | $$
| $$  | $$| $$$$$$$$| $$_/ $$_/ $$| $$  | $$|  \| $$$$$$$$| $$ | $$ | $$
| $$  | $$ \$$     \ \$$   $$   $$| $$   \$$  $$ \$$     \| $$ | $$ | $$
 \$$   \$$  \$$$$$$$  \$$$$$\$$$$  \$$    \$$$$   \$$$$$$$ \$$  \$$  \$$
'''


# Writing new Item to database
async def new_item(
        db_engine: AsyncEngine,
        admin_id: int,
        new_item_data: dict
):
    logger.info(f'new_item({new_item_data['name']})')

    len_catalogue: int  # Number of items in Catalogue table
    len_income: int  # Number of items in Income table

    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting length of Catalogue and Income tables
    len_catalogue_statement = (
        select(func.count())
        .select_from(catalogue)
    )
    len_income_statement = (
        select(func.count())
        .select_from(income)
    )

    async with db_engine.connect() as conn:
        raw_catalogue_len = await conn.execute(len_catalogue_statement)
        raw_income_len = await conn.execute(len_income_statement)
        for row in raw_catalogue_len:
            len_catalogue = int(row[0])
            logger.info(f'Catalogue table length is {len_catalogue}')
        for row in raw_income_len:
            len_income = int(row[0])
            logger.info(f'Income table length is {len_income}')

    # Writing statements for Catalogue and Income tables
    catalogue_statement = insert(catalogue).values(
        index=len_catalogue,
        category=new_item_data['category'],
        name=new_item_data['name'],
        description=new_item_data['description'],
        image=new_item_data['image'],
        self_price=new_item_data['self_price'],
        sell_price=new_item_data['sell_price'],
        count=new_item_data['count'],
    )

    income_statement = insert(income).values(
        index=len_income,
        admin_id=admin_id,
        date_and_time=date_and_time,
        item_index=len_catalogue,
        category=new_item_data['category'],
        name=new_item_data['name'],
        count=new_item_data['count'],
        income=int(new_item_data['count']) * int(new_item_data['sell_price']),
        pure_income=int(new_item_data['count']) * int(new_item_data['self_price']),
    )

    async with db_engine.connect() as conn:
        await conn.execute(catalogue_statement)
        await conn.execute(income_statement)
        await conn.commit()
        logger.info('New item in Catalogue and Income are commited')


# Deleting item from database
async def delete_item(
        db_engine: AsyncEngine,
        admin_id: int,
        ):
    logger.info(f'delete_item({admin_id})')
    page: int  # Current page of user from database

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == admin_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {admin_id}, page is {page}')

    # Delete current item
    delete_item_statement = (
        delete(catalogue)
        .where(catalogue.c.index == page)
    )

    # Commit to database
    async with db_engine.connect() as conn:
        await conn.execute(delete_item_statement)
        await conn.commit()
        logger.info(f'User {admin_id} deleted item #{page}')
    
    # Rewrite last index to deleted
    # Getting length of Edited tables
    len_catalogue_statement = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        raw_catalogue_len = await conn.execute(len_catalogue_statement)
        for row in raw_catalogue_len:
            len_catalogue = int(row[0])
            logger.info(f'Catalogue table length is {len_catalogue}')

    # Rewrite index of deleted position to catalogue len (last item)
    update_catalogue = (catalogue.update()
                        .values(index = page)
                        .where(catalogue.c.index == len_catalogue))
                    
    async with db_engine.connect() as conn:
        await conn.execute(update_catalogue)
        await conn.commit()



'''
                 __  __    __                                             
                |  \|  \  |  \                                            
  ______    ____| $$ \$$ _| $$_           ______    ______   __   __   __ 
 /      \  /      $$|  \|   $$ \         /      \  /      \ |  \ |  \ |  
|  $$$$$$\|  $$$$$$$| $$ \$$$$$$        |  $$$$$$\|  $$$$$$\| $$ | $$ | $$
| $$    $$| $$  | $$| $$  | $$ __       | $$   \$$| $$  | $$| $$ | $$ | $$
| $$$$$$$$| $$__| $$| $$  | $$|  \      | $$      | $$__/ $$| $$_/ $$_/ $$
 \$$     \ \$$    $$| $$   \$$  $$      | $$       \$$    $$ \$$   $$   $$
  \$$$$$$$  \$$$$$$$ \$$    \$$$$        \$$        \$$$$$$   \$$$$$\$$$$
'''

# Validate changes entered by Admin
def check_changes(changes: str) -> dict:
    logger.info(f'Checking for changes {changes}')
    changes_types = {
                     'category': str,
                     'name': str,
                     'description': str,
                     'image': str,
                     'sell_price': int,
                     'self_price': int,
                     'count': int
    }
    if changes[0] == '#':
        
        # drop #
        changes_raw = changes[1:].split()
        
        # is correct type of change
        if len(changes_raw) == 2 and changes_raw[0] in changes_types:
            
            logger.info(f'changes_raw[0]: {changes_raw[0]}')
            
            # unite changes description, like {'description': 'very taste banana'}
            if changes_raw[1].isdigit:
                changes_raw[1] = int(changes_raw[1])
                changes_united = {changes_raw[0]: changes_raw[1]}
            else:
                changes_united = {changes_raw[0]: ' '.join(changes_raw[1:])}
                
            logger.info(f'Changes raw: {changes_raw}')
            logger.info(f'changes_united: {changes_united}')
            logger.info(f'changes type {changes_types[changes_raw[0]]} is {type(changes_raw[1])}')
            
            # check for data type of changes
            if changes_types[changes_raw[0]] is type(changes_raw[1]):
                if changes_raw[0] == 'description' and len(changes_raw[1]) <= 624:
                    return changes_united
                elif (((changes_raw[0] == 'image')
                        and validators.url(changes_raw[1]))
                        or changes_raw[0] != 'image'):
                    return changes_united
                raise ValueError
            raise ValueError
        raise ValueError
    raise ValueError


# Writing changes of item in database
async def change_item(
        db_engine: AsyncEngine,
        admin_id: int,
        new_data: str
):
    logger.info(f'change_item({admin_id}, {new_data})')
    len_edited: int  # Number of items in Edited table
    page: int  # Current page of user from database

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == admin_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {admin_id}, page is {page}')

    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting length of Edited tables
    len_edited_statement = (
        select(func.count())
        .select_from(edited)
    )

    async with db_engine.connect() as conn:
        raw_edited_len = await conn.execute(len_edited_statement)
        for row in raw_edited_len:
            len_edited = int(row[0])
            logger.info(f'Catalogue table length is {len_edited}')

    # Getting item metadata
    item = await get_admin_item_metadata(
        int(page),
        db_engine
    )
    
    logger.info(f'Getted item metadata {item}')

    # Insert new row to Edited table
    edited_statement = insert(edited).values(
        index=len_edited,
        admin_id=admin_id,
        date_and_time=date_and_time,
        item_index=page,
        category=item['category'],
        name=item['name'],
        commit=(f'{type}: {new_data}')
    )

    # Update data in Catalogue table
    update_catalogue = (catalogue.update()
                        .values(**new_data)
                        .where(catalogue.c.index == page)
                        )

    async with db_engine.connect() as conn:
        await conn.execute(update_catalogue)
        await conn.execute(edited_statement)
        await conn.commit()
        logger.info(f'Users {admin_id} page is updated to {page}')


# Getting orders list by status
async def get_orders_list(
        db_engine: AsyncEngine,
        user_id: int,
        status: str
) -> list:
    orders_list = [] # Empty tuple for orders
    len_orders: int  # Checking for empty table

    logger.info(f'User {user_id} in getting order list with status {status}')

    len_orders_statement = (
        select(func.count())
        .select_from(orders)
        )
    
    async with db_engine.connect() as conn:
        raw_orders_len = await conn.execute(len_orders_statement)
        for row in raw_orders_len:
            len_orders = int(row[0])
            logger.info(f'Orders table length is {len_orders}')
    
    if len_orders != 0:  
        # Getting list of orders
        orders_list_statement = (select(column("index"), column("date_and_time"), 
                                column("name"), column("count"))
                                .select_from(orders)
                                .where(orders.c.status == status)
        )
        async with db_engine.connect() as conn:
            orders_raw = await conn.execute(orders_list_statement)
            for row in orders_raw:
                logger.info(f'Order data {list(row)}')
                orders_list.append(list(row))

        return orders_list
    else:
        return None


# Get order information
async def get_order_data(
        db_engine: AsyncEngine,
        order: int
) -> list:
    selected_order: list  # For putting order here 
    selected_order_statement = (
        select("*")
        .select_from(orders)
        .where(orders.c.index == int(order))
    )
    
    async with db_engine.connect() as conn:
        order_raw = await conn.execute(selected_order_statement)
        for row in order_raw:
            selected_order = tuple(row)
            logging.info(f'Selected order {order}')
            
    return selected_order

'''
                                                    __     
                                                   |  \    
  ______    _______   _______   ______    ______  _| $$_   
 |      \  /       \ /       \ /      \  /      \|   $$ \  
  \$$$$$$\|  $$$$$$$|  $$$$$$$|  $$$$$$\|  $$$$$$\$$$$$$  
 /      $$| $$      | $$      | $$    $$| $$  | $$ | $$ __ 
|  $$$$$$$| $$_____ | $$_____ | $$$$$$$$| $$__/ $$ | $$|  
 \$$    $$ \$$     \ \$$     \ \$$     \| $$    $$  \$$  $$
  \$$$$$$$  \$$$$$$$  \$$$$$$$  \$$$$$$$| $$$$$$$    \$$$$ 
                                        | $$               
                                        | $$               
                                         \$$                
'''


# Changing status for Accepted or Completed
async def change_order_status(
        i18n: TranslatorRunner,
        db_engine: AsyncEngine,
        user_id: int,
        order: int,
        updated_status: str
) -> str:
    logger.info(f'{updated_status} order {order} by {user_id}')
    costumer_id: int  # ID of costumer for sending notification
    coustumers_username: str  # @username of costumer for contact
    order_data: list  # Data of executed order
    
    # Get order data and update status
    order_data_statement = (select("*")
                            .select_from(orders)
                            .where(orders.c.index == order))
    
    update_status_statement = (orders.update()
                               .values(status=updated_status)
                               .where(orders.c.index == order)
                               )
    
    async with db_engine.connect() as conn:
        raw_order_data = await conn.execute(order_data_statement)
        await conn.execute(update_status_statement)
        await conn.commit()
        for row in raw_order_data:
            order_data = list(row)
            logger.info(f'User {user_id} executed order #{order} for {updated_status}')

    costumer_id = order_data[1]
    coustumers_username = order_data[2]
    
    # Init Bot
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Send notification to Customer
    if updated_status == 'accepted':
        await bot.send_message(chat_id=costumer_id,
                               text=i18n.order.accepted.notification(
                                    date_and_time=order_data[4],
                                    count=order_data[8],
                                    name=order_data[7],
                                    income=order_data[9]
                            ))
    
    elif updated_status == 'completed':
        len_outcome: int  # Number of items in Outcome Table
        
        await bot.send_message(chat_id=costumer_id,
                               text=i18n.order.completed.notification(
                                    date_and_time=order_data[4],
                                    count=order_data[8],
                                    name=order_data[7],
                                    income=order_data[9]
                           ))
        
        # Add order to Outcome table
        # Getting length of Outcome table
        len_outcome_statement = (
            select(func.count())
            .select_from(outcome)
        )
        
        # Updating Total Purchase Sum and Count in user data
        update_user = (users.update()
                       .values(purchase = users.c.purchase + 1,
                               purchase_sum = users.c.purchase_sum + order_data[9])
                       .where(users.c.telegram_id == int(costumer_id))
                       )
                    
        async with db_engine.connect() as conn:
            await conn.execute(update_user)
            await conn.commit()
            raw_outcome_len = await conn.execute(len_outcome_statement)
            for row in raw_outcome_len:
                len_outcome = int(row[0])
                logger.info(f'Outcome table length is {len_outcome}')
                
        outcome_statement = insert(catalogue).value(
            index=len_outcome,
            user_id=costumer_id,
            username=coustumers_username,
            date_and_time=order_data[4],
            item_index=order_data[5],
            category=order_data[6],
            name=order_data[7],
            count=order_data[8],
            income=order_data[9],
            pure_income=order_data[10]
            )
        
        
        async with db_engine.connect() as conn:
            await conn.execute(outcome_statement)
            await conn.commit()
            logger.info('New Order in Outcome commited')

    
    return coustumers_username


'''
       __                      __  __                     
      |  \                    |  \|  \                    
  ____| $$  ______    _______ | $$ \$$ _______    ______  
 /      $$ /      \  /       \| $$|  \|       \  /      \ 
|  $$$$$$$|  $$$$$$\|  $$$$$$$| $$| $$| $$$$$$$\|  $$$$$$
| $$  | $$| $$    $$| $$      | $$| $$| $$  | $$| $$    $$
| $$__| $$| $$$$$$$$| $$_____ | $$| $$| $$  | $$| $$$$$$$$
 \$$    $$ \$$     \ \$$     \| $$| $$| $$  | $$ \$$     
  \$$$$$$$  \$$$$$$$  \$$$$$$$ \$$ \$$ \$$   \$$  \$$$$$$$
'''



# Declining order
async def decline_order_process(
        i18n: TranslatorRunner,
        db_engine: AsyncEngine,
        user_id: int,
        order: int,
        reason: str
) -> str:
    logger.info(f'Declining order {order} by {user_id}')
    costumer_id: int  # ID of costumer for sending notification
    coustumers_username: str  # @username of costumer for contact
    order_data: list  # Data of executed order
    
    # Get order data and update status to Accepted
    order_data_statement = (select("*")
                            .select_from(orders)
                            .where(orders.c.index == order))
    
    update_status_statement = (catalogue.update()
                               .values(status='declined')
                               .where(orders.c.index == order)
                               )
    
    async with db_engine.connect() as conn:
        raw_order_data = await conn.execute(order_data_statement)
        await conn.execute(update_status_statement)
        await conn.commit()      
        for row in raw_order_data:
            order_data = list(row)
            logger.info(f'User {user_id} executed order #{order} for declining')
            
    # Returning count of declined items to Catalogue
    update_count_statement = (catalogue.update()
                              .values(count=(catalogue.c.count+order_data[8]))
                              .where(order.c.index == order))
    
    async with db_engine.connect() as conn:
        await conn.execute(update_count_statement)
        await conn.commit()
        logger.info(f'{order_data[8]} pieces of {order_data[7]} returned to Catalogue')

    costumer_id = order_data[1]
    coustumers_username = order_data[2]
    costumers_dict = get_user_data(int(costumer_id),
                                     db_engine)
    wallet = costumers_dict['address']
    income = order_data[9]
    
    # Init Bot
    bot_config = get_config(BotConfig, "bot")
    bot = Bot(token=bot_config.token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # Send notification to Customer
    await bot.send_message(chat_id=costumer_id,
                           text=i18n.order.declined.notification(
                               date_and_time=order_data[4],
                               count=order_data[8],
                               name=order_data[7],
                               income=order_data[9],
                               wallet=wallet,
                               reason=reason
                           ))
    
    return [coustumers_username, income, wallet]
    
    
# Parse selecting order for #number form
def check_order(order: str) -> str:
    logger.info(f'check_order{order}')
    if order[0] == '#' and order[1:].isdigit:
        return order
    raise ValueError  


