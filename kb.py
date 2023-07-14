'''Keyboards for bot'''
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#                           ReplyKeyboardRemove)
import text

main_menu_buttons = [
    [InlineKeyboardButton(text=text.BUTTON_SHOW_ID,
                          callback_data='show_id')],
    [InlineKeyboardButton(text=text.BUTTON_DEBUG,
                          callback_data='debug')],
    [InlineKeyboardButton(text=text.BUTTON_PARSER,
                          callback_data='parser')],
    [InlineKeyboardButton(text=text.BUTTON_HELP, callback_data='help')]
]
back_to_main_menu_button = InlineKeyboardButton(
    text=text.BUTTON_BACK_TO_MAIN_MENU,
    callback_data='main_menu')
back_to_parser_button = InlineKeyboardButton(
    text=text.BUTTON_BACK_TO_PARSER,
    callback_data='parser')
nav_parser_pre_button = InlineKeyboardButton(
    text=text.BUTTON_NAV_PARSER_PRE,
    callback_data='nav_parser_pre')
nav_parser_next_button = InlineKeyboardButton(
    text=text.BUTTON_NAV_PARSER_NEXT,
    callback_data='nav_parser_next')

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text.BUTTON_BACK_TO_MAIN_MENU)]],
    resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[back_to_main_menu_button]]
)
parser_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text.BUTTON_PARSER_PARAMS,
                              callback_data='parser_set_params')],
        [InlineKeyboardButton(text=text.BUTTON_PARSER_START,
                              callback_data='parser_start')],
        [back_to_main_menu_button]
    ]
)
parser_nav_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [nav_parser_pre_button, nav_parser_next_button],
        [back_to_parser_button],
        [back_to_main_menu_button]
    ]
)
parser_start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [nav_parser_next_button],
        [back_to_parser_button],
        [back_to_main_menu_button]
    ]
)
parser_end_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [nav_parser_pre_button],
        [back_to_parser_button],
        [back_to_main_menu_button]
    ]
)
parser_params_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text.BUTTON_PARSER,
                              callback_data='parser'),
         back_to_main_menu_button]
    ]
)
