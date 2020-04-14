import asyncio
import logging

import uvloop
from aiohttp import web

from todolist.logger import RequestsLogger
from todolist.settings import get_config
from todolist.app import init_app


def main():
    config = get_config()
    app = init_app(config)

    web.run_app(app,
                host=config.HOST,
                port=config.PORT)
    # TODO fix RequestsLogger error
    # access_log=RequestsLogger)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    main()
