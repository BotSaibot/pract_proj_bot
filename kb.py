from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

main_menu_buttons = [
    [InlineKeyboardButton(text='🆔 Мой идентификатор',
                          callback_data='show_id')],
    [InlineKeyboardButton(text='🔎 Помощь', callback_data='help')]
]

main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)
exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='◀️ Выйти в меню')]], resize_keyboard=True
)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='◀️ Выйти в меню',
                                           callback_data='main_menu')]]
)
