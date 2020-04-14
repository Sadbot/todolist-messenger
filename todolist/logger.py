import logging

from aiohttp.abc import AbstractAccessLogger

logging_level_for_modules = (
    ('pymorphy2.opencorpora_dict.wrapper', 'WARN')
)


def set_specific_logging_level():
    """
    Настраивает уровень логгирования у модулей, которые в лог пишут много не
    нужной информации
    :return:
    """
    for module, level in logging_level_for_modules:
        logging.getLogger(module).setLevel(level)


class RequestsLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        self.logger.info(f'{request.remote} '
                         f'"{request.method} {request.path} '
                         f'done in {time}s: {response.status}')


def init_logger(level: str, logger_name: str = None) -> logging.Logger:
    log = logging.getLogger(logger_name)
    log.setLevel(level)

    console_formatter = logging.Formatter(
        '#%(levelname)-s,%(name)s[%(filename)s]: %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    log.addHandler(console_handler)
    set_specific_logging_level()

    return log
