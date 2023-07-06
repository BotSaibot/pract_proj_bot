'''Handlers for bot'''
from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import kb
import text

router = Router()


@router.callback_query(F.data == 'show_id')
@router.message(Command('show_id'))
async def show_id_handler(message):
    '''Shows a user id'''
    text_out = text.TEXT_SHOW_ID.format(id=message.from_user.id,
                                        name=message.from_user.full_name)
    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.message(Command('start'))
async def start_handler(message: Message):
    '''Shows a greeting'''
    await message.answer(
        text.TEXT_GREET.format(name=message.from_user.full_name),
        reply_markup=kb.main_menu
    )


@router.callback_query(F.data == 'main_menu')
@router.message(Command('main_menu'))
async def main_menu_handler(message):
    '''Calls the main menu'''
    text_out = text.TEXT_MAIN_MENU_TITLE
    if isinstance(message, Message):
        await message.answer(text_out, reply_markup=kb.main_menu)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.main_menu)


@router.callback_query(F.data == 'help')
@router.message(Command('help'))
async def help_handler(message):
    '''Shows the help'''
    text_out = text.TEXT_HELP
    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == 'debug')
@router.message(Command('debug'))
async def debug_message_handler(message):
    '''Shows the debug message'''
    text_out = '⚙ This is debug message! ⚙'
    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)
