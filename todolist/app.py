import hashlib

from aiohttp import web

from todolist.db import init_pg, close_pg
from todolist.logger import init_logger
from todolist.middlewares import setup_middlewares
from todolist.routes import register_routes
from todolist.settings import BaseConfig


async def init_app(config: BaseConfig):
    logger = init_logger(config.LOGGER_LEVEL)

    app = web.Application()
    app['config'] = config
    app['logger'] = logger

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    # setup views and routes
    register_routes(app)

    setup_middlewares(app)

    return app
