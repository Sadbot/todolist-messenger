import logging
from todolist.drivers.dto import RequestMessage, ResponseMessage

from sqlalchemy.orm import Session
import sqlalchemy
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
    text_in = request.text.strip().lower()
    count_words = len(text_in.split())

    if count_words < 2:
        statement = sqlalchemy.sql.text(
            """select c.name  from public.command c WHERE c.is_active = true ORDER BY id """)
        result_proxy = session.execute(statement).fetchall()

    else:
        cmd = request.text.split()[1].lower()
        logger.debug(f'cmd: "{cmd}" ')
        statement = sqlalchemy.sql.text(
            """select c.name from public.command c 
               WHERE lower(c.name) LIKE :name and 
              c.is_active = true ORDER BY id """)
        cmd = '%' + cmd + '%'
        logger.info(f'cmd like: "{cmd}" ')
        result_proxy = session.execute(statement, {'name': cmd}).fetchall()

    i = 0
    for row in result_proxy:
        i = i + 1
        cmd = dict(row)
        name = cmd['name']
        logger.debug(f'Data "{name}"  ')
        text_ret = text_ret + str(i) + ') ' + name + '\n'

        components.add_button('run_task_name', value=name.lower(), text='Выполнить',
                              label=name)

    if i == 0:
        text_ret = text_ret + ' команды не найдены' + '\n'

    text_ret = text_ret + '\nДля выхода из диалога используйте: "выход", "выйти", "завершить", "закрыть", "отмена", "exit", "quit"\n'
    components.add_text(
        text='Для выхода из диалога используйте: "выход", "выйти", "завершить", "закрыть", "отмена", "exit", "quit"')

    return ResponseMessage(
        user_id=request.user_id,
        command_name='help',
        text=text_ret,
        photo=None,
        interactive_components=components
    )
