import logging

from sqlalchemy.orm import Session

from repositories.task_repository import TaskRepository
from todolist.drivers.dto import RequestMessage, ResponseMessage


async def todo_list(*, session: Session, request: RequestMessage, logger: logging.Logger = None,
                    **kwargs) -> ResponseMessage:
    """Тестовая команда проверки ответа.

    Args:
        request: объект сообщения запроса.
        logger: экземпляр логгера.

    Returns:
        Объект сообщения ответа.
    """
    logger = logger or logging.getLogger('command')
    logger.info(f'User "{request.user_id}" send todo_list command')

    text_ret = 'Список todo:\n'
    tasks = TaskRepository(session).get_available(request.user_id)

    if not tasks:
        text_ret = f'Нет активных задач!'

    for idx, task in enumerate(tasks):
        text_ret = f'{text_ret}{idx}: {task.text} ({task.use_date})\n'

    return ResponseMessage(
        user_id=request.user_id,
        command_name='todo_list',
        text=text_ret,
    )
