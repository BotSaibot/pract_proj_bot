'''Handlers for bot'''
import sys
import logging
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.methods.delete_message import DeleteMessage
from aiogram.types import Message

import kb
import text
import bs4_based_parser
import params

HANDLERS_PARAMS = {}

router = Router()

logger = logging.getLogger(__name__)


class FSMParser(StatesGroup):
    '''State group for the parser'''
    active = State()
    go_to_page = State()
    set_params = State()


async def process_cancel(state: FSMContext, user_id: str):
    '''process cancel state'''
    current_state = await state.get_state()

    if current_state is None:
        return
    if current_state in ('FSMParser:go_to_page', 'FSMParser:set_params'):
        user_params = HANDLERS_PARAMS[user_id]
        user_params['message_history'].clear()

    await state.clear()


async def continue_res(parser_params: dict) -> tuple:
    '''Continues to get a result for the parser'''
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


@router.callback_query(F.data == 'debug', StateFilter(default_state))
@router.message(Command('debug'), StateFilter(default_state))
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
async def main_menu_handler(message, state: FSMContext):
    '''Calls the main menu'''
    layouts = text.layouts[main_menu_handler.__name__]
    await process_cancel(state, message.from_user.id)

    if isinstance(message, Message):
        await message.answer(layouts['text'], reply_markup=kb.main_menu)
    else:
        await message.message.edit_text(
            layouts['text'], reply_markup=kb.main_menu)


@router.callback_query(
    F.data == 'nav_go_to_page', StateFilter(FSMParser.active))
async def parser_go_to_page_handler(message, state: FSMContext):
    '''Goes to a page'''
    layouts = text.layouts[parser_go_to_page_handler.__name__]
    user_params = HANDLERS_PARAMS[message.from_user.id]

    await state.set_state(FSMParser.go_to_page)
    amt = user_params['parser_params']['total_pages']
    text_out = layouts['text'].format(amt=amt)
    await message.answer(text_out.translate(text_out.maketrans(
        dict(zip('&<lt;</b>', ['<'] + [None] * 8)))))
    ans = await message.message.answer(text_out)
    user_params.setdefault('message_history', []).extend(
        [(ans.chat.id, ans.message_id),
         (message.message.chat.id, message.message.message_id)])


@router.callback_query(
    F.data == 'parser', StateFilter(default_state, FSMParser.active))
@router.message(Command('parser'))
async def parser_menu_handler(message, state: FSMContext):
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
        await state.set_state(FSMParser.active)
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=kb.parser_menu_kb)


@router.callback_query(
    F.data == 'parser_set_params', StateFilter(FSMParser.active))
async def parser_set_params(message, state: FSMContext):
    '''Sets parser's parametrs'''
    layouts = text.layouts[parser_set_params.__name__]
    user_params = HANDLERS_PARAMS[message.from_user.id]
    text_out = (
        layouts['text'] + '\n\n' + layouts['example1'] + '\n\n'
        + layouts['example2'])
    user_params.setdefault('message_history', []).append(
        (message.message.chat.id, message.message.message_id))
    await state.set_state(FSMParser.set_params)
    await message.message.edit_text(text_out)


@router.callback_query(F.data == 'show_id')
@router.message(Command('show_id'))
async def show_id_handler(message, state: FSMContext):
    '''Shows a user id'''
    layouts = text.layouts[show_id_handler.__name__]
    text_out = layouts['text'].format(
        id=message.from_user.id, name=message.from_user.full_name,
        status=await state.get_state())

    if isinstance(message, Message):
        await message.answer(text_out)
    else:
        await message.message.edit_text(text_out, reply_markup=kb.iexit_kb)


@router.callback_query(F.data.in_(
    ('parser_start', 'nav_parser_next', 'nav_parser_pre', 'nav_parser_to_end',
     'nav_parser_to_start')),
    StateFilter(FSMParser.active),
    flags={'chat_action': 'typing'})
async def parser_handler(message):
    '''Shows the parser message'''
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

    response = await continue_res(parser_params)

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
        reply_markup = await kb.get_nav_parser_bottom_kb(
            'start', parser_params.get('page') + 1, total_pages)
        parser_params.update([('total_pages', total_pages)])
    elif parser_params.get('page') + 1 == total_pages:
        reply_markup = await kb.get_nav_parser_bottom_kb(
            'end', parser_params.get('page') + 1, total_pages)
    else:
        reply_markup = await kb.get_nav_parser_bottom_kb(
            'normal', parser_params.get('page') + 1, total_pages)

    if ismessage:
        await message.answer(
            text_out, disable_web_page_preview=True,
            reply_markup=reply_markup)
    else:
        await message.message.edit_text(
            text_out, disable_web_page_preview=True,
            reply_markup=reply_markup)


@router.callback_query(
    F.data.startswith('nav_transition_failure'), StateFilter(FSMParser.active))
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
async def cancel_handler(message: Message, state: FSMContext):
    '''Cancels current command'''
    layouts = text.layouts[cancel_handler.__name__]
    status = await state.get_state()
    await process_cancel(state, message.from_user.id)
    await message.answer(layouts['text'].format(status))


@router.message(Command('start'), StateFilter(default_state))
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


@router.message(StateFilter(FSMParser.set_params, FSMParser.go_to_page))
async def process_set_params(message: Message, state: FSMContext):
    '''Handles user's messages with parameters'''
    user_params = HANDLERS_PARAMS[message.from_user.id]
    message_history = user_params['message_history']
    mode = await state.get_state()
    layouts = text.layouts[process_set_params.__name__][mode]
    mode = mode == 'FSMParser:set_params'
    failure, failure_msg, failure_try = False, None, text.layouts['try_again']

    try:

        if mode:
            new_params = await bs4_based_parser.decoder_str_to_params(
                message.text, layouts)
        else:
            page = await bs4_based_parser.decoder_str_to_page(
                message.text, layouts,
                user_params['parser_params']['total_pages'])

    except AssertionError as error:
        failure_msg = error.args[0]
        failure = True

    if not failure:

        if mode:
            await state.clear()
            user_params['parser_params'] = new_params
        else:
            await state.set_state(FSMParser.active)
            user_params['parser_params']['page'] = page

        message_history.append((message.chat.id, message.message_id))

        if mode:
            await message.answer(
                layouts['text'], reply_markup=kb.parser_params_kb)
        else:
            await parser_handler(message)

        for chat_id, message_id in message_history:
            await DeleteMessage(chat_id=chat_id, message_id=message_id)

        message_history.clear()
    else:
        ans = await message.answer(f'{failure_msg} {failure_try}')
        message_history.extend([(ans.chat.id, ans.message_id),
                                (message.chat.id, message.message_id)])
