'''Handlers for bot'''
from aiogram import F, Router
from aiogram.types import Message  # CallbackQuery
from aiogram.filters import Command
import logging

import kb
import text
import bs4_based_parser

HANDLERS_PARAMS = {}

router = Router()

logger = logging.getLogger(__name__)


async def check_params(id):
    '''Checks handler's parameters by id.'''
    logger.info('check_params() is running...')
    if id not in HANDLERS_PARAMS:

        HANDLERS_PARAMS[id] = {'status': None, 'parser_params': {}}


@router.callback_query(F.data == 'debug')
@router.message(Command('debug'))
async def debug_message_handler(message):
    '''Shows the debug message'''
    text_out = '⚙ This is debug message! ⚙\n```\n'

    if isinstance(message, Message):
        await message.answer(
            text_out + message.json(indent=4, exclude_none=True) + '\n```'
        )
    else:
        await message.message.edit_text(
            text_out + message.json(indent=4, exclude_none=True) + '\n```',
            reply_markup=kb.iexit_kb
        )


@router.callback_query(F.data == 'help')
@router.message(Command('help'))
async def help_handler(message):
    '''Shows the help'''
    text_out = text.TEXT_HELP
    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == 'main_menu')
@router.message(Command('main_menu'))
async def main_menu_handler(message):
    '''Calls the main menu'''
    text_out = text.TEXT_MAIN_MENU_TITLE
    if isinstance(message, Message):
        await message.answer(text_out, reply_markup=kb.main_menu)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.main_menu)


@router.callback_query(F.data == 'parser')
@router.message(Command('parser'))
async def parser_menu_handler(message):
    '''Shows the parser menu'''
    await check_params(message.from_user.id)
    text_out = '\n'.join(
        [bs4_based_parser.__doc__,
         'URL = ' + bs4_based_parser.RESOURCE_URL,
         'HEADER = ' + ''.join(str(i) for i
                               in bs4_based_parser.RESOURCE_HEADER.items()),
         'PARAMS = '
         + ''.join(
             str(i) for i
             in HANDLERS_PARAMS[message.from_user.id]['parser_params'].items()
         )]
    )

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_menu_kb
        )


# @router.callback_query(F.data == 'parser_start', 'nav_parser_next')
@router.callback_query(F.data.in_(('parser_start', 'nav_parser_next')))
@router.message(Command('parser_start'))
async def parser_handler(message):
    '''Shows the parser message'''
    await check_params(message.from_user.id)

    response = await bs4_based_parser.get_response(
        url=bs4_based_parser.RESOURCE_URL,
        headers=bs4_based_parser.RESOURCE_HEADER,
        params=HANDLERS_PARAMS[message.from_user.id]['parser_params']
    )

    # response = parser.tree_traversal(response, params)
    host, results, total_pages = await bs4_based_parser.get_general_info(
        response, HANDLERS_PARAMS[message.from_user.id]['parser_params']
    )

    if isinstance(message, Message):

        text_out = f'{host} -> Finded {results}, total pages {total_pages}'
        await message.answer(text_out, disable_web_page_preview=True)

    else:

        response = await bs4_based_parser.simply_traversal(response, host)

        text_out = []
        for index, value in response.items():
            key, name, area, salary, url, employer = value.values()

            out = (f'''[{index}] {key} {url}\n\t{name}\n\t'''
                   f''''{employer}', {area}\n\t{salary}\n''')

            text_out.append(out)

        bottom = ['―' * 31,
                  f'{host} -> Finded {results}, total pages {total_pages}',
                  f'message data {message.data!r}']
        text_out.extend(bottom)

        text_out = '\n'.join(text_out)

        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_nav_kb
        )


@router.callback_query(F.data == 'parser_params')
async def parser_params(message):
    '''Sets parser's parametrs'''
    await check_params(message.from_user.id)

    text_out = (text.TEXT_PARSER_PARAMS + '\n\n'
                + text.TEXT_PARSER_PARAMS_EXAMPLE1 + '\n\n'
                + text.TEXT_PARSER_PARAMS_EXAMPLE2)

    HANDLERS_PARAMS.setdefault(
        message.from_user.id, {}
    )['status'] = 'edit_params'

    await message.message.answer(text_out)


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


@router.message(Command('cancel'))
async def cancel_handler(message: Message):
    '''Cancels current command'''
    await check_params(message.from_user.id)
    HANDLERS_PARAMS.setdefault(message.from_user.id, {})['status'] = None
    await message.answer('The command `/cancel` is done')


@router.message(Command('start'))
async def start_handler(message: Message):
    '''Shows a greeting'''
    await message.answer(
        text.TEXT_GREET.format(name=message.from_user.full_name),
        reply_markup=kb.main_menu
    )

    await check_params(message.from_user.id)


@router.message()
async def message_handler(message: Message):
    '''Handles user's messages'''
    await check_params(message.from_user.id)

    if (HANDLERS_PARAMS.setdefault(message.from_user.id,
                                   {'status': None})['status']
            == 'edit_params'):
        new_params = await bs4_based_parser.decoder_str_to_params(message.text)
        HANDLERS_PARAMS[message.from_user.id]['status'] = None
        HANDLERS_PARAMS[message.from_user.id]['parser_params'] = new_params
        await message.answer(text.TEXT_PARSER_PARAMS_SUCCESS,
                             reply_markup=kb.parser_params_kb)
