from aiogram.fsm.state import State, StatesGroup

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
