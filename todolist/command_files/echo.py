import logging
from todolist.drivers.dto import RequestMessage, ResponseMessage


async def echo(*, request: RequestMessage, logger: logging.Logger = None, **kwargs) -> ResponseMessage:
    """Тестовая команда проверки ответа.

    Args:
        request: объект сообщения запроса.
        logger: экземпляр логгера.

    Returns:
        Объект сообщения ответа.
    """
    logger = logger or logging.getLogger('command')
    logger.info(f'User "{request.user_id}" send Echo command')
    text_to_ret = request.text
    if text_to_ret == '':
        text_to_ret = 'Эхо: Введите любой текст'

    return ResponseMessage(
        user_id=request.user_id,
        command_name='echo',
        text=text_to_ret,
        photo=None,
        interactive_components=None
    )
