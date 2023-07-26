'''Handlers for bot'''
import sys
import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.methods.delete_message import DeleteMessage
from aiogram.types import Message

import kb
import text
import bs4_based_parser
import params

HANDLERS_PARAMS = {}

router = Router()

logger = logging.getLogger(__name__)


# async def check_params(user_id):
#     '''Checks handler's parameters by id.'''
#     logger.info('check_params() is running...')
#     HANDLERS_PARAMS.update(params.load_params())
#     if user_id not in HANDLERS_PARAMS:
#         HANDLERS_PARAMS[user_id] = {'status': None, 'parser_params': {},
#                                     'message_history': []}
#         params.unload_params(HANDLERS_PARAMS)


@router.callback_query(F.data == 'debug')
@router.message(Command('debug'))
async def debug_message_handler(message):
    '''Shows the debug message'''
    layouts = text.layouts[debug_message_handler.__name__]
    text_out = (f'{layouts["text"]}\n'
                f'<pre>{message.json(indent=4, exclude_none=True)}</pre>')

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == 'help')
@router.message(Command('help'))
async def help_handler(message):
    '''Shows the help'''
    layouts = text.layouts[help_handler.__name__]

    if isinstance(message, Message):
        await message.answer(layouts['text'])
    else:
        await message.message.edit_text(
            layouts['text'], reply_markup=kb.iexit_kb)


@router.callback_query(F.data == 'main_menu')
@router.message(Command('main_menu'))
async def main_menu_handler(message):
    '''Calls the main menu'''
    layouts = text.layouts[main_menu_handler.__name__]

    if isinstance(message, Message):
        await message.answer(layouts['text'], reply_markup=kb.main_menu)
    else:
        await message.message.edit_text(
            layouts['text'], reply_markup=kb.main_menu)


@router.callback_query(F.data == 'nav_go_to_page')
async def parser_go_to_page_handler(message):
    '''Goes to a page'''
    layouts = text.layouts[parser_go_to_page_handler.__name__]
    user_params = HANDLERS_PARAMS[message.from_user.id]
    user_params['status'] = 'go_to_page'
    amt = user_params['parser_params']['total_pages']
    text_out = layouts['text'].format(amt=amt)
    await message.answer(text_out.translate(text_out.maketrans(
        dict(zip('&<lt;</b>', ['<'] + [None] * 8)))))
    ans = await message.message.answer(text_out)
    user_params.setdefault('message_history', []).extend(
        [ans.message_id, message.message.message_id])


@router.callback_query(F.data == 'parser')
@router.message(Command('parser'))
async def parser_menu_handler(message):
    '''Shows the parser menu'''
    user_params = HANDLERS_PARAMS.setdefault(
        message.from_user.id, {'parser_params': {}})
    text_out = '\n'.join(
        [bs4_based_parser.__doc__,
         f'<pre>URL = {bs4_based_parser.RESOURCE_URL}',
         f'HEADER = {str(bs4_based_parser.RESOURCE_HEADER)}',
         f'PARAMS = {user_params.setdefault("parser_params", {})}</pre>'])

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_menu_kb)


@router.callback_query(F.data == 'parser_set_params')
async def parser_set_params(message):
    '''Sets parser's parametrs'''
    layouts = text.layouts[parser_set_params.__name__]
    text_out = (
        layouts['text'] + '\n\n' + layouts['example1'] + '\n\n'
        + layouts['example2'])
    HANDLERS_PARAMS[message.from_user.id]['status'] = 'edit_params'
    await message.message.answer(text_out)


@router.callback_query(F.data == 'show_id')
@router.message(Command('show_id'))
async def show_id_handler(message):
    '''Shows a user id'''
    layouts = text.layouts[show_id_handler.__name__]
    text_out = layouts['text'].format(
        id=message.from_user.id, name=message.from_user.full_name,
        status=HANDLERS_PARAMS.setdefault(
            message.from_user.id,
            {'status': None}).setdefault('status', None))
    # text_out += f'\nПараметры: {HANDLERS_PARAMS[message.from_user.id]}'

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.callback_query(F.data.in_(
    ('parser_start', 'nav_parser_next', 'nav_parser_pre', 'nav_parser_to_end',
     'nav_parser_to_start')), flags={'chat_action': 'typing'})
async def parser_handler(message):
    '''Shows the parser message'''
    async def continue_res():
        response = await bs4_based_parser.get_response(
            url=bs4_based_parser.RESOURCE_URL,
            headers=bs4_based_parser.RESOURCE_HEADER,
            params=parser_params
        )

        if isinstance(response, str):
            return response

        host, results, total_pages = await bs4_based_parser.get_general_info(
            response, parser_params
        )
        return host, results, total_pages, response

    layouts = text.layouts[parser_handler.__name__]
    parser_params = HANDLERS_PARAMS[message.from_user.id]['parser_params']
    ismessage = isinstance(message, Message)

    if ismessage or message.data == 'parser_start':
        parser_params.setdefault('page', 0)
        parser_params.setdefault('items_on_page', 5)
    elif message.data == 'nav_parser_next':
        parser_params.update([('page', parser_params['page'] + 1)])
    elif message.data == 'nav_parser_to_end':
        parser_params.update(
            [('page', parser_params.get('total_pages') - 1)])
    elif message.data == 'nav_parser_to_start':
        parser_params.update([('page', 0)])
    elif (message.data == 'nav_parser_pre'
          and parser_params.get('page') is not None
          and parser_params.get('page') > 0):
        parser_params.update([('page', parser_params['page'] - 1)])

    parser_params.update([('hhtmFrom', 'vacancy_search_list')])

    response = await continue_res()

    if isinstance(response, str):
        text_out = response
        total_pages = parser_params['total_pages']
    else:
        host, results, total_pages, response = response
        response = await bs4_based_parser.simply_traversal(response, host)

        text_out = []

        for index, value in response.items():
            index = (parser_params.setdefault('page', 0)
                     * parser_params['items_on_page'] + index)
            values = list(value.values())
            text_out.append(layouts['text'].format(index, *values))

        text_out.append(layouts['bottom'].format(
            '―' * 22, host, results, parser_params['items_on_page']))
        text_out = '\n'.join(text_out)

    if parser_params.get('page') == 0:
        reply_markup = await kb.get_nav_parser_kb(
            'start', parser_params.get('page') + 1, total_pages)
        parser_params.update([('total_pages', total_pages)])
    elif parser_params.get('page') + 1 == total_pages:
        reply_markup = await kb.get_nav_parser_kb(
            'end', parser_params.get('page') + 1, total_pages)
    else:
        reply_markup = await kb.get_nav_parser_kb(
            'normal', parser_params.get('page') + 1, total_pages)

    if ismessage:
        await message.answer(
            text_out, disable_web_page_preview=True,
            reply_markup=reply_markup)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=reply_markup)


@router.callback_query(F.data.startswith('nav_transition_failure'))
async def parser_nav_transition_failure(message):
    '''Informs about the failure and it's reason'''
    layouts = text.layouts[parser_nav_transition_failure.__name__]
    failure_reason = message.data.removeprefix('nav_transition_failure:')

    if failure_reason in ('pre', 'start'):
        text_out = layouts['pre_start']
    elif failure_reason in ('next', 'end'):
        text_out = layouts['next_end']
    else:
        text_out = layouts['other']

    await message.answer(text_out)


@router.message(Command('cancel'))
async def cancel_handler(message: Message):
    '''Cancels current command'''
    layouts = text.layouts[cancel_handler.__name__]
    user_params = HANDLERS_PARAMS.setdefault(
        message.from_user.id, {'status': None})
    status = user_params['status']

    if status == 'go_to_page':
        user_params['message_history'].clear()

    user_params['status'] = None
    await message.answer(layouts['text'].format(status))


@router.message(Command('start'))
async def start_handler(message: Message):
    '''Shows a greeting'''
    layouts = text.layouts[start_handler.__name__]
    await message.answer(
        layouts['text'].format(name=message.from_user.full_name),
        reply_markup=kb.main_menu
    )


@router.message(Command('stop'))
async def stop_handler(message):
    '''Stops the bot'''
    await message.answer('Shotdowning')
    params.unload_params(HANDLERS_PARAMS)
    sys.exit(0)


@router.message()
async def message_handler(message: Message):
    '''Handles user's messages'''
    layouts = text.layouts[message_handler.__name__]
    user_params = HANDLERS_PARAMS.setdefault(
        message.from_user.id, {'status': None})
    failure, failure_msg, failure_try = False, None, layouts['try']

    if user_params['status'] == 'edit_params':
        layouts = layouts[user_params['status']]
        try:
            new_params = await bs4_based_parser.decoder_str_to_params(
                message.text, layouts)
        except AssertionError as error:
            failure_msg = error.args[0]
            failure = True

        if not failure:
            user_params['status'] = None
            user_params['parser_params'] = new_params
            await message.answer(layouts['text'],
                                 reply_markup=kb.parser_params_kb)
        else:
            await message.answer(f'{failure_msg} {failure_try}')

    elif user_params['status'] == 'go_to_page':
        layouts = layouts[user_params['status']]
        message_history = user_params['message_history']
        try:
            page = await bs4_based_parser.decoder_str_to_page(
                message.text, layouts,
                user_params['parser_params']['total_pages'])
        except AssertionError as error:
            failure_msg = error.args[0]
            failure = True

        if not failure:
            user_params['status'] = None
            user_params['parser_params']['page'] = page
            message_history.append(message.message_id)
            await parser_handler(message)

            for pre_message in message_history:
                await DeleteMessage(chat_id=message.chat.id,
                                    message_id=pre_message)

            message_history.clear()
        else:
            ans = await message.answer(f'{failure_msg} {failure_try}')
            message_history.extend([message.message_id, ans.message_id])
