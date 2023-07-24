'''The main module.'''
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import HANDLERS_PARAMS, router
from params import load_params


async def main():
    '''The main function'''
    bot = Bot(token=config.TG_T, parse_mode=ParseMode.HTML)
    disp = Dispatcher(storage=MemoryStorage())
    disp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    HANDLERS_PARAMS.update(load_params())
    await disp.start_polling(bot,
                             allowed_updates=disp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('[%(asctime)s:%(msecs)03d] [%(filename)s:%(lineno)d] '
                '%(levelname)s:%(name)s:%(message)s'),
        datefmt='%d.%m.%Y %H:%M:%S'
    )
    asyncio.get_event_loop().run_until_complete(main())
