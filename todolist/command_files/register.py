import logging

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from todolist.models import MsgUser
from todolist.drivers.dto import ResponseMessage, RequestMessage

COMMAND_NAME_EN = 'register'
COMMAND_NAME_RU = 'регистрация'


async def register(*, session: Session, request: RequestMessage, logger: logging.Logger = None, **kwargs) -> ResponseMessage:
    """Команда регистрации пользователя.

    Args:
        session: открытая сессия БД.
        request: объект сообщения запроса.
        logger: экземпляр логгера.

    Returns:
        Объект сообщения ответа.
    """
    logger = logger or logging.getLogger('command')

    if not request.email and not request.phone and not request.username:
        logger.warning('The ReguestMessage object does not contain a phone or email or username')
        text = 'При регистрации произошла ошибка. Пожалуйста, попробуйте, позже.'

    elif is_user_already_registered(session=session,
                                    messenger_type=request.messenger_type,
                                    user_id=request.user_id,
                                    email=request.email,
                                    username=request.username,
                                    phone=request.phone):
        text = 'Пользователь с такими данными уже зарегистрирован.'
        logger.info(
            f'User with phone "{request.phone}" or email "{request.email}"  or username "{request.username}"  is already registered')

    else:
        text = 'Пользователь зарегистрирован.'
        session.add(MsgUser(
            email=request.email, username=request.username, ext_id=request.user_id, phone=request.phone,
            messenger_type_id=request.messenger_type))
        session.commit()
        logger.info(f'User "{request.user_id}" successfully registered')

    return ResponseMessage(
        user_id=request.user_id,
        command_name=COMMAND_NAME_EN,
        text=text,
        photo=None,
        interactive_components=None
    )


def is_user_already_registered(session: Session, messenger_type: int, user_id: str, email: str = None, username: str = None,
                               phone: str = None) -> bool:
    """Проверка. зарегистрирован ли пользователь с переданными данными.

    Args:
        session: сессия соединения с БД.
        messenger_type: идентификатор месенджера.
        user_id: идентификатор пользователя.
        email: адрес эл. почты пользователя.
        phone: номер телефона пользователя.

    Returns:
        True если пользователь уже зарегистрирован, иначе False.
    """
    or_query_args = [MsgUser.ext_id == str(user_id)]

    if email:
        or_query_args.append(MsgUser.email == email)

    if username:
        or_query_args.append(MsgUser.username == username)

    if phone:
        or_query_args.append(MsgUser.phone == phone)

    return bool(session.query(MsgUser).filter(
        and_(
            or_(*or_query_args),
            MsgUser.messenger_type_id == messenger_type
        )
    ).all())
