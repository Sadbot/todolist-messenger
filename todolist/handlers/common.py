import logging
from typing import Any, List, Optional

from sqlalchemy.orm import Session

from todolist.command_files.echo import echo
from todolist.drivers.dto import RequestMessage, ResponseMessage
from todolist.handlers.dialog import UserDialog
from todolist.models.command import Command
from todolist.repositories.command_repository import CommandRepository
from todolist.repositories.user_repository import UserRepository
from todolist.utils.morph_analyzer import MorphAnalyzer
from todolist.components.builder import InteractiveComponentsBuilder


class CommonHandler:
    COMMAND_FUNCTIONS = {
        'echo': echo,
    }

    def __init__(self, db: Session, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger('common_handler')
        self.db: Session = db

        self._commands = None
        self._request = None
        self._user = None

    async def _call_command(self, command: Command, user_dialog: UserDialog = None) -> ResponseMessage:
        """Вызов функции команды.

        Args:
            command: экземпляр команды.
            user_dialog: экземпляр диалога пользователя.

        Returns:
            Экземпляр ответного сообщения.
        """
        if command.filename is not None:
            command_func_ = self.COMMAND_FUNCTIONS.get(command.filename)
            if not command_func_:
                self.logger.warning(
                    f'невозможно найти команду {command.name}, '
                    f'файл отсутвует, вместо неё запуститься echo')
                command_func_ = echo

            return await command_func_(
                session=self.db,
                request=self._request,
                user_dialog=user_dialog,
                command_id=command.id,
                logger=self.logger
            )

        return self._get_response(text=command.response_text, command_name=command.name)

    def _get_command_by_name_and_text(self, text: str = None, name: str = None) -> Optional[Command]:
        """Получение функции команды по имени и тексту.

        Args:
            text: текст команды.
            name: имя команды.

        Returns:
            Функция команды.
        """
        # ищем команду по имени
        if name and self._commands.get(name.lower()):
            return self._commands.get(name.lower())

        if text:
            # ищем по всему тексту на совпадение с именем
            cmd_name = text.lower()
            self.logger.debug(f'cmd_name is {cmd_name}')
            if self._commands.get(cmd_name):
                return self._commands[cmd_name]

            # если не нашли, поищем по первому слову из текста на совпадение с именем
            cmd_name_short = text.partition(' ')[0].lower()
            self.logger.debug(f'cmd_name_short is {cmd_name_short}')
            if self._commands.get(cmd_name_short):
                return self._commands[cmd_name_short]

    def _get_command_name_by_id(self, command_id: int) -> Optional[str]:
        """Получение имени команды по идентификатору.

        Args:
            command_id: идентификатор команды.

        Returns:
            Название команды.
        """
        for command_name, command in self._commands.items():
            if command_id == command.id:
                return command_name

    def _get_commands_by_keywords(self) -> List[Command]:
        """Получение команд по ключевым словам.

        Returns:
            Список найденных команд.
        """
        commands = []
        norm_list = MorphAnalyzer(logger=self.logger).analyze_list_normal_words(self._request.text)
        self.logger.debug(f'norm_list: {norm_list}')

        if norm_list:
            commands = CommandRepository(self.db, self.logger).get_commands_by_keywords(keywords=norm_list)

        return commands

    def _get_response(self, text: str = '', command_name: str = '', user_id: str = None, photo: str = None,
                      components: InteractiveComponentsBuilder = None) -> ResponseMessage:
        """Получение экземпляра ответного сообщения.

        Args:
            text: текст сообщения.
            command_name: название команды.
            user_id: идентификатор пользователя.
            photo: информация об изображении.
            components: интерактивные компоненты.

        Returns:
            Экземпляр ответного сообщения.
        """
        return ResponseMessage(
            user_id=user_id or self._request.user_id,
            command_name=command_name,
            text=text,
            photo=photo,
            interactive_components=components
        )

    async def _handle_open_dialog(self, user_dialog: UserDialog) -> ResponseMessage:
        """
        Обработка сообщения диалога пользователя.

        Args:
            user_dialog: экземпляр диалога.

        Returns:
            Экземпляр ответного сообщения.
        """
        if self._is_close_dialog_command():
            user_dialog.close()
            return self._get_response(text='Диалог завершен')

        dialog_command = self._get_command_name_by_id(command_id=user_dialog['command_id'])

        if not dialog_command:
            return self._get_response(text='Ошибка открытия диалога')

        # если пользователь вызвал команду при открытом диалоге
        if self._request.command_name:
            return self._get_response(text=f'Есть открытый диалог команды "{dialog_command}"')

        command = self._commands[dialog_command]
        return await self._call_command(command=command, user_dialog=user_dialog)

    def _is_close_dialog_command(self) -> bool:
        """Проверка, что сообщение является командой закрытия диалога.

        Returns:
            True если сообщение на закрытие диалога, иначе False.
        """
        return self._request.text.lower() in ['выход', 'выйти', 'завершить', 'закрыть', 'отмена', 'exit', 'quit']

    def _is_inactive_user(self) -> bool:
        """Проверка что пользователь не активен.

        Returns:
            True если пользователь существует и не активен, иначе False.
        """
        return self._user and (not self._user.is_user_active or not self._user.is_um_active)

    @staticmethod
    def _is_register_command(command: Command) -> bool:
        """Проверка, что вызванная команда является регистрацией.

        Args:
            command: объект команды.

        Returns:
            True если команда это команда регистрации, иначе False.
        """
        return command.filename == REGISTER_COMMAND_NAME

    async def dispatch(self, request: RequestMessage) -> ResponseMessage:
        """Обработка входящего сообщения.

        Args:
            request: экземпляр сообщения запроса.

        Returns:
            Экземпляр ответного сообщения.
        """
        self.logger.debug(f'request: {request}')
        self._request = request
        self._user = UserRepository(self.db).get_full_user_info(request.user_id, request.messenger_type)
        self._commands = CommandRepository(self.db).get_available_dict()
        self.logger.debug(f'Found user {self._user}')

        if not self._user:
            command = self._get_command_by_name_and_text(text=request.text, name=request.command_name)
            self.logger.info(f'Found command {command}')
            if command and self._is_register_command(command):
                return await self._call_command(command=command)

            return self._get_response(
                text='Чтобы начать общение, необходимо зарегистрироваться. Отправь команду "Регистрация"',
                command_name='')

        elif self._is_inactive_user():
            return self._get_response(text='Ваша учетная запись не активна, обратитесь к администратору')

        user_dialog = UserDialog(user_id=self._user.id, db_session=self.db, data=self._user.dialog_data)
        self.logger.debug(f'User dialog - {user_dialog}')

        # если есть открытый диалог
        if user_dialog.is_open():
            return await self._handle_open_dialog(user_dialog=user_dialog)

        # если пришло нажатие кнопки для выполнения команды из help
        if (request.actions and request.actions[0]['action_id'] == 'run_task_name'
                and self._commands.get(request.actions[0]['value'])):
            command = self._commands[request.actions[0]['value']]
            return await self._call_command(command=command, user_dialog=user_dialog)

        self.logger.debug(f'Command name is {self._request.command_name}')
        command = self._get_command_by_name_and_text(text=request.text, name=request.command_name)
        if command and self._is_register_command(command):
            return self._get_response(text='Вы уже зарегистрированы', command_name='')

        if command:
            return await self._call_command(command=command, user_dialog=user_dialog)

        # если в запросе нет команды или нет точного совпадения, то ищем по нормализованым ключевым словам
        available_commands = self._get_commands_by_keywords()

        if not available_commands:
            return self._get_response(text='Команда не найдена. Введите помощь (help) для вывода доступных команд')

        if len(available_commands) > 1:
            text = ', '.join([command.name for command in available_commands])
            components = InteractiveComponentsBuilder()
            for command in available_commands:
                components.add_button('run_task_name', value=command.name.lower(), text='Выполнить',
                                      label=command.name)

            return self._get_response(text=f'Найдено несколько команд по запросу: {text}', components=components)

        return await self._call_command(command=available_commands[0], user_dialog=user_dialog)
