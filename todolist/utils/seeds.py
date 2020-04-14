import logging

from sqlalchemy.orm import scoped_session


def make_seeds_if_empty(db_session_manager: scoped_session, logger: logging.Logger):
    session = db_session_manager()
    logger.info('start update seeds')

    logger.info('end update seeds')
