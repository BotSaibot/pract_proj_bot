'''Handlers for bot'''
from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import kb
import text
import bs4_based_parser

HANDLERS_PARAMS = {}

router = Router()


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
    text_out = '\n'.join(
        [bs4_based_parser.__doc__,
         'URL = ' + bs4_based_parser.RESOURCE_URL,
         'HEADER = ' + ''.join(str(i) for i
                               in bs4_based_parser.RESOURCE_HEADER.items()),
         'PARAMS = ' + ''.join(str(i) for i in HANDLERS_PARAMS.items())]
    )

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_menu_kb
        )


@router.callback_query(F.data == 'parser_none')
@router.message(Command('parser_none'))
async def parser_handler(message):
    '''Shows the parser message'''
    params = {
        'text': 'python',
        'part_time': 'temporary_job_true',
        'professional_role': 96,
        'search_field': ['name', 'company_name', 'description'],
        'enable_snippets': False,
        'salary': 270_000,
        # 'items_on_page': 20,
        'items_on_page': 2,
        'only_with_salary': True,
        'ored_clusters': True,
        'order_by': 'publication_time',
        'status': 'non_archived'
    }

    response = bs4_based_parser.get_response(
        url=bs4_based_parser.RESOURCE_URL,
        headers=bs4_based_parser.RESOURCE_HEADER,
        params=params
    )

    # response = parser.tree_traversal(response, params)
    host, results, total_pages = bs4_based_parser.get_general_info(
        response, params
    )
    response = bs4_based_parser.simply_traversal(response, host)

    text_out = []
    for index, value in response.items():
        key, name, area, salary, url, employer = value.values()

        out = (f'''[{index}] {key} {url}\n\t{name}\n\t'''
               f''''{employer}', {area}\n\t{salary}\n''')

        text_out.append(out)

    F_data = message.data
    text_out.extend(['―'*31, f'{results = }', f'{total_pages = }',
                     f'{F_data = }'])

    text_out = '\n'.join(text_out)

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_nav_kb
        )


@router.callback_query(F.data == 'parser_params')
async def parser_params(message):
    '''Sets parser's parametrs'''
    text_out = (text.TEXT_PARSER_PARAMS + '\n\n'
                + text.TEXT_PARSER_PARAMS_EXAMPLE1)
    
    HANDLERS_PARAMS.setdefault(message.from_user.id, {})['status'] = 'edit_params'

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
    HANDLERS_PARAMS.setdefault(message.from_user.id, {})['status'] = None
    await message.answer('The command `/cancel` is done')


@router.message(Command('start'))
async def start_handler(message: Message):
    '''Shows a greeting'''
    await message.answer(
        text.TEXT_GREET.format(name=message.from_user.full_name),
        reply_markup=kb.main_menu
    )

    if message.from_user.id not in HANDLERS_PARAMS:

        HANDLERS_PARAMS[message.from_user.id] = {
            'status': None,
            'parser_params': None
        }


@router.message()
async def message_handler(message: Message):
    '''Handles user's messages'''
    if (HANDLERS_PARAMS.setdefault(message.from_user.id,
                                   {'status': None})['status']
        == 'edit_params'):
        ...

        HANDLERS_PARAMS[message.from_user.id]['status'] = None
