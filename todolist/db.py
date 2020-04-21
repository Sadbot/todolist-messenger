import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from todolist.settings import BaseConfig
from utils.seeds import make_seeds_if_empty


async def init_pg(app):
    config: BaseConfig = app['config']
    logger: logging.Logger = app['logger']
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    db_session_manager = scoped_session(sessionmaker(bind=engine))

    make_seeds_if_empty(db_session_manager, logger)

    app['db'] = db_session_manager


async def close_pg(app):
    app['db'].close()
