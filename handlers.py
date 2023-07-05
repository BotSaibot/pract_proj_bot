from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import kb
import text

router = Router()


@router.callback_query(F.data == 'show_id')
@router.message(Command('show_id'))
async def message_handler(message):
    obj = message if isinstance(message, Message) else message.message
    await obj.answer(text.show_id.format(id=message.from_user.id,
                                         debug=type(message).__qualname__))


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(text.greet.format(name=message.from_user.full_name),
                     reply_markup=kb.main_menu)


@router.callback_query(F.data == 'main_menu')
@router.message(F.text == 'Меню')
@router.message(F.text == 'Выйти в меню')
@router.message(F.text == '◀️ Выйти в меню')
async def call_main_menu(message):
    obj = message if isinstance(message, Message) else message.message
    await obj.answer(text.main_menu_title, reply_markup=kb.main_menu)


@router.callback_query(F.data == 'help')
@router.message(Command('help'))
async def start_handler(message):
    obj = message if isinstance(message, Message) else message.message
    await obj.answer(text.help, reply_markup=kb.iexit_kb)
