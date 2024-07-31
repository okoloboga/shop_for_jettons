from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluentogram import TranslatorRunner


# Main keyboard
def play_account_kb(i18n: TranslatorRunner):
    button_play = InlineKeyboardButton(text=i18n.play(),
                                       callback_data='play')
    button_account = InlineKeyboardButton(text=i18n.stats(),
                                          callback_data='stats')
    button_back = InlineKeyboardButton(text=i18n.button.back(),
                                       callback_data='total_back')
    return InlineKeyboardMarkup(inline_keyboard=[[button_play], [button_account], [button_back]])


# Canceling waiting for enemy
def back_kb(i18n: TranslatorRunner):
    button_back = InlineKeyboardButton(text=i18n.back(),
                                       callback_data='back')
    return InlineKeyboardMarkup(inline_keyboard=[[button_back]])


# Confirm game
def create_join_kb(i18n: TranslatorRunner):
    button_create = InlineKeyboardButton(text=i18n.create.button(),
                                         callback_data='create')
    button_join = InlineKeyboardButton(text=i18n.join.button(),
                                       callback_data='join')
    button_back = InlineKeyboardButton(text=i18n.back(),
                                       callback_data='back')
    return InlineKeyboardMarkup(inline_keyboard=[[button_create, button_join], [button_back]])


# Enemy select
def select_enemy(rooms: dict, i18n: TranslatorRunner) -> InlineKeyboardMarkup:
    button_back = InlineKeyboardButton(text=i18n.back(),
                                       callback_data='back')
    buttons_enemy = []
    print(rooms)
    for key in rooms:
        buttons_enemy.append(
            [InlineKeyboardButton(text=i18n.button.rooms(user_id=key[2:], bet=rooms[key]),
                                  callback_data=(str(key[2:] + ' ' + rooms[key])))])
    buttons_enemy.append([button_back])
    return InlineKeyboardMarkup(inline_keyboard=buttons_enemy)


# Confirming game with joined enemy
def game_confirm(i18n: TranslatorRunner):
    button_confirm = InlineKeyboardButton(text=i18n.great(),
                                          callback_data='game_confirm')
    return InlineKeyboardMarkup(inline_keyboard=[[button_confirm]])


# Main game keyboard
def game_process_kb(i18n: TranslatorRunner):
    button_1 = InlineKeyboardButton(text=i18n.rock(),
                                    callback_data='rock')
    button_2 = InlineKeyboardButton(text=i18n.scissors(),
                                    callback_data='scissors')
    button_3 = InlineKeyboardButton(text=i18n.paper(),
                                    callback_data='paper')
    button_end_game = InlineKeyboardButton(text=i18n.end.game(),
                                           callback_data='end_game')
    return InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_end_game]])


# Confirm leaved enemy
def enemy_leaved_ok(i18n: TranslatorRunner):
    button_ok = InlineKeyboardButton(text=i18n.great(),
                                     callback_data='back')
    return InlineKeyboardMarkup(inline_keyboard=[[button_ok]])


# Bets keyboard
def bet_kb(i18n: TranslatorRunner):
    button_1 = InlineKeyboardButton(text=i18n.b1(),
                                    callback_data='b1')
    button_2 = InlineKeyboardButton(text=i18n.b2(),
                                    callback_data='b2')
    button_3 = InlineKeyboardButton(text=i18n.b3(),
                                    callback_data='b3')
    button_4 = InlineKeyboardButton(text=i18n.b4(),
                                    callback_data='b4')
    button_5 = InlineKeyboardButton(text=i18n.b5(),
                                    callback_data='b5')
    button_25 = InlineKeyboardButton(text=i18n.b25(),
                                     callback_data='b25')
    button_back = InlineKeyboardButton(text=i18n.back(),
                                       callback_data='back')
    return InlineKeyboardMarkup(
        inline_keyboard=[[button_1, button_2, button_3, button_4], [button_5, button_25], [button_back]])


# Enter jettons value
def digit_inline(i18n: TranslatorRunner):
    button_back = InlineKeyboardButton(text=i18n.back(),
                                       callback_data='back')
    digit_keyboard = []
    for j in range(3):
        digit_keyboard.append(
            [InlineKeyboardButton(text=str(i + j * 3 + 1), callback_data=str(i + j * 3 + 1)) for i in range(3)])

    digit_keyboard.append([InlineKeyboardButton(text='<', callback_data='<'),
                           InlineKeyboardButton(text='0', callback_data='0'),
                           InlineKeyboardButton(text='ok', callback_data='ok')])
    digit_keyboard.append([button_back])

    return InlineKeyboardMarkup(inline_keyboard=digit_keyboard)


# Checking for opponents turn
def check_kb(i18n: TranslatorRunner):
    button = InlineKeyboardButton(text=i18n.button.check(),
                                  callback_data='check')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
