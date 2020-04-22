import logging

from repositories.command_repository import CommandRepository
from todolist.drivers.dto import RequestMessage, ResponseMessage

from sqlalchemy.orm import Session
from todolist.components.builder import InteractiveComponentsBuilder


async def help(*, session: Session, request: RequestMessage, logger: logging.Logger = None,
               **kwargs) -> ResponseMessage:
    """Команда помощи

    Args:
        request: объект сообщения запроса.
        logger: экземпляр логгера.

    Returns:
        Объект сообщения ответа.
    """
    logger = logger or logging.getLogger('command')
    logger.info(f'User "{request.user_id}" send help command')
    components = InteractiveComponentsBuilder()
    text_ret = 'Команды:\n'
    request_word_count = len(request.text.strip().split())
    command_rep = CommandRepository(session)

    if request_word_count == 1:
        commands_list = command_rep.get_active()
    else:
        logger.debug(f'command_name: "{request.command_name}" ')
        commands_list = command_rep.find_by_name(request.command_name)
        logger.info(f'command_name like: "{request.command_name}" ')

    if not commands_list:
        text_ret = text_ret + ' команды не найдены' + '\n'

    for idx, row in enumerate(commands_list):
        logger.debug(f'Data "{row.name}"  ')
        text_ret = f'{text_ret}/{row.filename} {row.name} \n'

        components.add_button('run_task_name', value=row.filename.lower(), text='Выполнить',
                              label=row.name)

    text_ret = f'{text_ret}\nДля выхода из диалога используйте: ' \
               f'"выход", "выйти", "завершить", "закрыть", "отмена", "exit", "quit"\n'
    components.add_text(
        text='Для выхода из диалога используйте: "выход", "выйти", "завершить", "закрыть", "отмена", "exit", "quit"')

    return ResponseMessage(
        user_id=request.user_id,
        command_name='help',
        text=text_ret,
        photo=None,
        interactive_components=components
    )
