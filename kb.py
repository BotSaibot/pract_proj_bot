'''Keyboards for bot'''
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
import text

main_menu_buttons = [
    [InlineKeyboardButton(text=text.BUTTON_SHOW_ID,
                          callback_data='show_id')],
    [InlineKeyboardButton(text=text.BUTTON_DEBUG,
                          callback_data='debug')],
    [InlineKeyboardButton(text=text.BUTTON_HELP, callback_data='help')]
]

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text.BUTTON_BACK_TO_MAIN_MENU)]],
    resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=text.BUTTON_BACK_TO_MAIN_MENU,
                                           callback_data='main_menu')]]
)
