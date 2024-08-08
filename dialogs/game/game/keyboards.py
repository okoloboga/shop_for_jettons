from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluentogram import TranslatorRunner


# Main game keyboard
def game_process_kb(i18n: TranslatorRunner):
    button_1 = InlineKeyboardButton(text=i18n.rock(),
                                    callback_data='rock')
    button_2 = InlineKeyboardButton(text=i18n.scissors(),
                                    callback_data='scissors')
    button_3 = InlineKeyboardButton(text=i18n.paper(),
                                    callback_data='paper')
    button_leave_game = InlineKeyboardButton(text=i18n.leave.game(),
                                           callback_data='leave_game')
    return InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_leave_game]])


# Confirm leaved enemy
def game_confirm_kb(i18n: TranslatorRunner):
    button_ok = InlineKeyboardButton(text=i18n.great(),
                                     callback_data='back')
    return InlineKeyboardMarkup(inline_keyboard=[[button_ok]])


# Checking for opponents turn
def check_kb(i18n: TranslatorRunner):
    button = InlineKeyboardButton(text=i18n.button.check(),
                                  callback_data='check')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


# Ending Game after result
def game_end(i18n: TranslatorRunner):
    button = InlineKeyboardButton(text=i18n.button.endgame(),
                                  callback_data='end_game')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


