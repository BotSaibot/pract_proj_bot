'''Keyboards for bot'''
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#                           ReplyKeyboardRemove)
from text import buttons

main_menu_buttons = [
    [InlineKeyboardButton(text=buttons['show id'],
                          callback_data='show_id')],
    [InlineKeyboardButton(text=buttons['debug'],
                          callback_data='debug')],
    [InlineKeyboardButton(text=buttons['parser']['main'],
                          callback_data='parser')],
    [InlineKeyboardButton(text=buttons['help'], callback_data='help')]
]
back_to_main_menu_button = InlineKeyboardButton(
    text=buttons['back to']['main menu'],
    callback_data='main_menu')
back_to_parser_button = InlineKeyboardButton(
    text=buttons['back to']['parser'],
    callback_data='parser')

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=buttons['back to']['main menu'])]],
    resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[back_to_main_menu_button]]
)
parser_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=buttons['parser']['params'],
                              callback_data='parser_set_params')],
        [InlineKeyboardButton(text=buttons['parser']['start'],
                              callback_data='parser_start')],
        [back_to_main_menu_button]
    ]
)
parser_params_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=buttons['parser']['main'],
                              callback_data='parser'),
         back_to_main_menu_button]
    ]
)


async def get_nav_parser_kb(option: str, page, total_page: int):
    '''Gives a navigational keyboard of the parser.
    option: str - type of a navigational keyboard,
    page: int - current page number,
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
        text=buttons['parser']['nav']['next'],
        callback_data=callback_data_nav_parser_next)
    nav_parser_pre_button = InlineKeyboardButton(
        text=buttons['parser']['nav']['pre'],
        callback_data=callback_data_nav_parser_pre)
    nav_parser_to_end_button = InlineKeyboardButton(
        text=buttons['parser']['nav']['go to']['end'],
        callback_data=callback_data_nav_parser_to_end)
    nav_parser_to_page_button = InlineKeyboardButton(
        text=buttons['parser']['nav']['go to']['page'].format(
            page=page, pages=total_page),
        callback_data='nav_go_to_page')
    nav_parser_to_start_button = InlineKeyboardButton(
        text=buttons['parser']['nav']['go to']['start'],
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
