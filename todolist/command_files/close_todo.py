import logging

from sqlalchemy.orm import Session

from todolist.drivers.dto import RequestMessage, ResponseMessage
from todolist.models import User
from todolist.repositories.task_repository import TaskRepository


async def add_todo(*, session: Session, request: RequestMessage, logger: logging.Logger = None,
                   user: User, **kwargs) -> ResponseMessage:
    """Тестовая команда проверки ответа.

    Args:
        request: объект сообщения запроса.
        logger: экземпляр логгера.

    Returns:
        Объект сообщения ответа.
    """
    logger = logger or logging.getLogger('command')
    logger.info(f'User "{request.user_id}" send add_todo command')

    tasks = TaskRepository(session).get_available(request.user_id)

    if not tasks:
        text_ret = f'Нет активных задач!'

    for idx, task in enumerate(tasks):
        pass

    return ResponseMessage(
        user_id=request.user_id,
        command_name='todo_list',
        text=text_ret,
    )