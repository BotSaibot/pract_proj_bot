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
parser_params_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=text.BUTTON_PARSER,
                              callback_data='parser'),
         back_to_main_menu_button]
    ]
)


async def get_nav_parser_kb(option: str, page, total_page: int):
    '''Gives a navigational keyboard of the parser.
    option: str - type of a navigational keyboard,
    page: int - сurrent page number,
    total_page: int - total number of pages.'''

    if option == 'normal':

        callback_data_nav_parser_next = 'nav_parser_next'
        callback_data_nav_parser_pre = 'nav_parser_pre'
        callback_data_nav_parser_to_end = 'nav_parser_to_end'
        callback_data_nav_parser_to_start = 'nav_parser_to_start'

    elif option == 'start':

        callback_data_nav_parser_next = 'nav_parser_next'
        callback_data_nav_parser_pre = 'nav_transition_failure:pre'
        callback_data_nav_parser_to_end = 'nav_parser_to_end'
        callback_data_nav_parser_to_start = 'nav_transition_failure:start'

    elif option == 'end':

        callback_data_nav_parser_next = 'nav_transition_failure:next'
        callback_data_nav_parser_pre = 'nav_parser_pre'
        callback_data_nav_parser_to_end = 'nav_transition_failure:end'
        callback_data_nav_parser_to_start = 'nav_parser_to_start'

    nav_parser_next_button = InlineKeyboardButton(
        text=text.BUTTON_NAV_PARSER_NEXT,
        callback_data=callback_data_nav_parser_next)
    nav_parser_pre_button = InlineKeyboardButton(
        text=text.BUTTON_NAV_PARSER_PRE,
        callback_data=callback_data_nav_parser_pre)
    nav_parser_to_end_button = InlineKeyboardButton(
        text=text.BUTTON_NAV_PARSER_GO_TO_END,
        callback_data=callback_data_nav_parser_to_end)
    nav_parser_to_page_button = InlineKeyboardButton(
        text=text.BUTTON_NAV_GO_TO_PAGE.format(page=page, pages=total_page),
        callback_data='nav')
    nav_parser_to_start_button = InlineKeyboardButton(
        text=text.BUTTON_NAV_PARSER_GO_TO_START,
        callback_data=callback_data_nav_parser_to_start)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [nav_parser_to_start_button, nav_parser_pre_button,
             nav_parser_to_page_button, nav_parser_next_button,
             nav_parser_to_end_button],
            [back_to_parser_button],
            [back_to_main_menu_button]
        ]
    )

    return keyboard
