import logging

from sqlalchemy.orm import scoped_session

from drivers.dto import SLACK_MESSENGER, TELEGRAM_MESSENGER
from todolist.models import MessengerType, Command


def make_seeds_if_empty(db_session_manager: scoped_session, logger: logging.Logger):
    session = db_session_manager()
    logger.info('start update seeds')

    if not session.query(MessengerType).first():
        logger.info(f'Run seeds for {MessengerType.__tablename__}')
        objects = [
            MessengerType(id=SLACK_MESSENGER, name="slack"),
            MessengerType(id=TELEGRAM_MESSENGER, name="telegram")
        ]
        session.bulk_save_objects(objects)
        session.commit()

    if not session.query(Command).first():
        logger.info(f'Run seeds for {Command.__tablename__}')
        objects = [
            Command(name="Эхо", filename="echo", keywords1='эхо', is_active=True),
            Command(name="Регистрация", filename="register", keywords1='регистрация',
                    is_active=True),
            Command(name="Помощь", keywords1='помощь, help', keywords2='бот, команда',
                    filename='help', is_active=True
                    ),
        ]
        session.bulk_save_objects(objects)
        session.commit()

    logger.info('end update seeds')
