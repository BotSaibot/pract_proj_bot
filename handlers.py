'''Handlers for bot'''
import logging
from aiogram import F, Router
from aiogram.types import Message  # CallbackQuery
from aiogram.filters import Command

import kb
import text
import bs4_based_parser

HANDLERS_PARAMS = {}

router = Router()

logger = logging.getLogger(__name__)


async def check_params(user_id):
    '''Checks handler's parameters by id.'''
    logger.info('check_params() is running...')
    if user_id not in HANDLERS_PARAMS:

        HANDLERS_PARAMS[user_id] = {'status': None, 'parser_params': {}}


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


@router.callback_query(F.data.in_(('parser_start', 'nav_parser_next',
                                   'nav_parser_pre', 'nav_parser_to_end',
                                   'nav_parser_to_start')))
@router.message(Command('parser_start'))
async def parser_handler(message):
    '''Shows the parser message'''
    await check_params(message.from_user.id)
    parser_params = (
        HANDLERS_PARAMS[message.from_user.id]['parser_params'])

    async def continue_res():
        response = await bs4_based_parser.get_response(
            url=bs4_based_parser.RESOURCE_URL,
            headers=bs4_based_parser.RESOURCE_HEADER,
            params=parser_params
        )

        host, results, total_pages = await bs4_based_parser.get_general_info(
            response, parser_params
        )
        return host, results, total_pages, response

    if isinstance(message, Message):

        host, results, total_pages, response = await continue_res()
        await message.answer((f'{host} -> Finded {results}, '
                              f'total pages {total_pages}'),
                             disable_web_page_preview=True)

    else:

        if message.data == 'nav_parser_next':

            parser_params.update(
                [('page', parser_params.setdefault('page', 0) + 1),
                 ('hhtmFrom', 'vacancy_search_list')])

        elif message.data == 'nav_parser_to_end':

            parser_params.update(
                [('page', parser_params.get('total_pages') - 1),
                 ('hhtmFrom', 'vacancy_search_list')])

        elif message.data == 'nav_parser_to_start':

            parser_params.update(
                [('page', 0), ('hhtmFrom', 'vacancy_search_list')])

        elif (message.data == 'nav_parser_pre'
              and parser_params.get('page') is not None
              and parser_params.get('page') > 0):

            parser_params.update(
                [('page', parser_params.setdefault('page', 0) - 1),
                 ('hhtmFrom', 'vacancy_search_list')])

        host, results, total_pages, response = await continue_res()
        response = await bs4_based_parser.simply_traversal(response, host)

        text_out = []
        for index, value in response.items():
            index = (parser_params.setdefault('page', 0)
                     * parser_params.setdefault('items_on_page', 20) + index)
            key, name, area, salary, url, employer = value.values()

            text_out.append(f'''[{index}] {key} {url}\n\t{name}\n\t'''
                            f''''{employer}', {area}\n\t{salary}\n''')

        text_out.extend(
            ['―' * 22,
             f'{host} -> Finded {results}, total pages {total_pages}',
             f'message data {message.data!r}\n'
             f'page {parser_params.get("page") + 1}'])

        text_out = '\n'.join(text_out)

        if parser_params.get('page') == 0:

            # reply_markup = kb.parser_start_kb
            reply_markup = await kb.get_nav_parser_kb(
                'start', parser_params.get('page') + 1, total_pages)
            parser_params.update([('total_pages', total_pages)])

        elif parser_params.get('page') + 1 == total_pages:

            # reply_markup = kb.parser_end_kb
            reply_markup = await kb.get_nav_parser_kb(
                'end', parser_params.get('page') + 1, total_pages)

        else:

            # reply_markup = kb.parser_nav_kb
            reply_markup = await kb.get_nav_parser_kb(
                'normal', parser_params.get('page') + 1, total_pages)

        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=reply_markup
        )


@router.callback_query(F.data == 'parser_set_params')
async def parser_set_params(message):
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

    if HANDLERS_PARAMS[message.from_user.id]['status'] == 'edit_params':
        new_params = await bs4_based_parser.decoder_str_to_params(message.text)
        HANDLERS_PARAMS[message.from_user.id]['status'] = None
        HANDLERS_PARAMS[message.from_user.id]['parser_params'] = new_params
        await message.answer(text.TEXT_PARSER_PARAMS_SUCCESS,
                             reply_markup=kb.parser_params_kb)
