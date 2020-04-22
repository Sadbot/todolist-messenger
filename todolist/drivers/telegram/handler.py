import logging
from functools import partial

from aiogram import Dispatcher, types
from aiogram.types import ContentType
from sqlalchemy.orm import Session

from todolist.components.interactive import Button
from todolist.drivers.dto import RequestMessage, TELEGRAM_MESSENGER
from todolist.handlers.command_handler import CommandHandler


def register_handlers(dp: Dispatcher, logger: logging.Logger):
    """
    Подключение общего обработчика на все сообщения
    """
    handler = partial(default_handler, db_session=dp['db'], logger=logger)
    dp.register_message_handler(handler, content_types=ContentType.ANY)


async def default_handler(message: types.Message, db_session: Session, logger: logging.Logger):
    """
    Подключение обработчика запросов общего для всех мессенджеров
    """
    request_message = hydrate_request(message)
    response = await CommandHandler(db_session, logger).dispatch(request_message)

    markup = types.ReplyKeyboardRemove()
    if response.interactive_components:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for component in response.interactive_components:
            if isinstance(component, Button):
                markup.add(component.value)

    if response.text:
        await message.reply(response.text,
                            reply_markup=markup,
                            parse_mode='Markdown')
    elif response.photo:
        await message.reply_photo(response.photo, reply_markup=markup)


def hydrate_request(message: types.Message) -> RequestMessage:
    """
    Генерация DTO запроса на основании входного сообщения.
    """
    command_name = None
    text_strip = message.text.strip()
    if text_strip.startswith('/'):
        command_name, *_ = text_strip.split(maxsplit=1)
        command_name = command_name.strip('/')

    return RequestMessage(
        user_id=str(message.from_user.id),
        text=message.text,
        dialog_id=message.chat.id,
        messenger_type=TELEGRAM_MESSENGER,
        command_name=command_name,
        username=message.from_user.username,
    )
