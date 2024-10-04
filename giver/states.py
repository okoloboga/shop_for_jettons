from aiogram.fsm.state import State, StatesGroup

# Users States

class MainSG(StatesGroup):
    fill_eth = State()
    fill_sol = State()
    fill_trx = State()
    select_coin = State()
    account = State()