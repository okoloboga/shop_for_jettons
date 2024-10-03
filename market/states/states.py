from aiogram.fsm.state import State, StatesGroup

# Users States

class StartSG(StatesGroup):
    start = State()
    start_previous = State()
    start_next = State()
    show_item = State()

class AccountSG(StatesGroup):
    is_new = State()
    account = State()
    input_refcode = State()
    already_invited = State()
    refcode_complete = State()
    refcode_error = State()


class NewUserSG(StatesGroup):
    new_user = State()


class CatalogueSG(StatesGroup):
    catalogue = State()


class WantSG(StatesGroup):
    want = State()
    fill_count = State()
    fill_address = State()
    confirm = State()
    complete = State()
    
# Admins States

class ItemSG(StatesGroup):
    start = State()
    start_previous = State()
    start_next = State()
    show_item = State()


class Admin_CatalogueSG(StatesGroup):
    catalogue = State()


class Admin_StartSG(StatesGroup):
    main = State()


class AddRowSG(StatesGroup):
    add_row = State()
    fill_category = State()
    fill_name = State()
    fill_description = State()
    fill_image = State()
    fill_price_count = State()
    confirm = State()
    complete = State()


class EditRowSG(StatesGroup):
    edit_row = State()
    edit = State()
    delete = State()
    new_data = State()
    delete_confirmed = State()
    changes_confirmed = State()


class ConfirmOrderSG(StatesGroup):
    select_status = State()
    select_order = State()
    new_order = State()
    accept_order = State()
    decline_order = State()
    status_changed = State()
    accepted_order = State()
    declined_order = State()
    completed_order = State()


# Game Lobby states
class LobbySG(StatesGroup):
    main = State()
    create_join = State()
    make_bet = State()
    wait_game = State()
    select_enemy = State()
    game_confirm = State()

# Game Process state
class GameSG(StatesGroup):
    main = State()

