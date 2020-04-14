import logging

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from todolist.db import close_pg
from todolist.drivers.telegram.handler import register_handlers
from todolist.logger import init_logger
from todolist.settings import get_config


def create_dispatcher():
    config = get_config()
    logger = init_logger(config.LOGGER_LEVEL)

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    db_session = scoped_session(sessionmaker(bind=engine))

    # TODO Add db with proxies and iterate by available connections
    # proxy = 'socks5://185.251.10.153:1080'
    # proxy = 'socks5://50.62.35.16:38950'
    proxy = 'socks5://96.96.33.133:1080'

    bot = Bot(token=config.TELEGRAM_TOKEN, proxy=proxy)
    dispatcher = Dispatcher(bot)
    dispatcher['config'] = config
    dispatcher['db'] = db_session  # аналогично тому, как создаётся в init_pg функции

    register_handlers(dispatcher, logger)

    return dispatcher


if __name__ == '__main__':
    dp = create_dispatcher()
    executor.start_polling(dp,
                           on_shutdown=close_pg,
                           skip_updates=True)
