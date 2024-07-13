import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.tables import users
from services import (get_admin_item_metadata, delete_item, 
                      change_item, get_user_data)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show selected item from catalogue for editing or deleting
async def edit_delete_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    user_id = user_dict['user_id']
    page = await get_user_data(user_id, db_engine)
    item_id = page['page']

    logger.info(f'User {user_id} select item №{item_id} from catalogue')

    # Rewrite User page to ITEM_ID
    update_page = (users.update()
                   .values(page=item_id)
                   .where(users.c.telegram_id == user_id)
                   )
    # Commit to database
    async with db_engine.connect() as conn:
        await conn.execute(update_page)
        await conn.commit()
        logger.info(f'Users {user_id} page is updated to {item_id}')

    # Getting data of item from new Users page
    item = await get_admin_item_metadata(int(item_id), db_engine)

    return {"button_back": i18n.button.back(),
            "button_delete": i18n.button.delete(),
            "button_edit": i18n.button.edit(),
            "button_confirm": i18n.button.confirm(),
            "delete_confirm": i18n.delete.confirm(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            ),
            "item_show": i18n.admin.item.show(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            )
            }


# Chosing changes to fill
async def select_type_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    # Getting page of user
    user_dict = dialog_manager.start_data
    user_id = user_dict['user_id']
    user_data = await get_user_data(user_id, db_engine)
    
    # Getting data of item from Users page
    item = await get_admin_item_metadata(int(user_data['page']), db_engine)
        
    return {"button_back": i18n.button.back(),
            "button_category": i18n.button.category(),
            "button_name": i18n.button.name(),
            "button_description": i18n.button.description(),
            "button_image": i18n.button.image(),
            "button_sellprice": i18n.button.sellprice(),
            "button_selfprice": i18n.button.selfprice(),
            "button_count": i18n.button.count(),
            "edit_menu": i18n.edit.menu(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            )
            }


# Filling changes of selected type
async def fill_changes_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    return {"button_back": i18n.button.back(),
            "enter_new_data": i18n.fill.newdata()
            }


# Deleting confirmed
async def delete_confirmed_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    user_id = user_dict['user_id']

    logger.info(f'User {user_id} confirmed item deleting')

    await delete_item(
        db_engine,
        user_id
    )

    return {
        "delete_complete": i18n.delete.complete(),
        "button_back": i18n.button.back()
    }


# Changes confirmed
async def changes_confirmed_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    user_id = user_dict['user_id']
    new_data = dialog_manager.current_context().dialog_data['new_data']
    feature = dialog_manager.current_context().dialog_data['change']

    logger.info(f'User {user_id} confirmed item changes')

    await change_item(
        db_engine,
        user_id,
        new_data,
        feature
    )

    return {
        "changes_complete": i18n.changes.complete(),
        "button_back": i18n.button.back()
    }
