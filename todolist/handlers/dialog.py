"""Модуль для управления диалогами пользователей.
Актуальное состояние диалога хранится в БД.

Пример использования:
    dialog = UserDialog(user_id=<user_id>, db_session=<db_session>)

    # for open new dialog
    dialog.open(command_id=<command_id>)

    # adds dialog values
    dialog['str_field'] = 'value'
    dialog['list_field'] = [1, 2, 3]
    dialog['dict_field'] = {'one': 1, 'two': 2}
    dialog['bool_field'] = True

    # save actual dialog
    dialog.save()

    # close open dialog
    dialog.close()
"""
import logging
import json
from typing import Any, Dict, Union

from sqlalchemy import null
from sqlalchemy.orm import Session

from todolist.models.user import MsgUser


class UserDialog(dict):
    def __init__(self, user_id: int, db_session: Session, logger: logging.Logger = None,
                 data: Union[Dict[str, Any], str] = None) -> None:
        """
        Args:
            user_id: идентификатор пользователя.
            db_session: открытая сессия с БД.
            logger: экземпляр логгера.
            data: данные диалога.
        """
        super().__init__()

        self.logger = logger or logging.getLogger('dialog')
        self.user_id = user_id
        self._session = db_session
        self._user_info = None

        self._initialize_data(data)

    @property
    def _user(self) -> MsgUser:
        """Свойство для получения экземпляра пользователя из БД.

        Returns:
            Экземпляр объекта пользователя.

        Raises:
            ValueError если пользователь с указанным идентификатором не найден в БД.
        """
        if self._user_info is None:
            self._user_info = self._session.query(MsgUser).filter(MsgUser.id == self.user_id).first()
            if self._user_info is None:
                raise ValueError(f'User with id {self.user_id} not found in database')

        return self._user_info

    def close(self) -> None:
        """Закрывает диалог пользователя. Удаляет данные диалога из БД.

        Raises:
            RuntimeError если диалог уже закрыт.
        """
        if self._user.dialog_data is None:
            raise RuntimeError(f'Dialog for user "{self.user_id}" already close.')

        self.logger.info(f'Close dialog for user "{self.user_id}"')
        self._save(data=null())

    def is_open(self) -> bool:
        """Проверка открыт ли у пользователя диалог.

        Returns:
            True если диалог открыт, иначе False.
        """
        return bool(self._user.dialog_data)

    def open(self, command_id: int) -> None:
        """Открывает диалог пользователя сохраняя в БД текущие данные диалога.

        Raises:
            RuntimeError если диалог уже открыт.
        """
        if self._user.dialog_data:
            raise RuntimeError(f'Dialog for user "{self.user_id}" already open.')

        self['command_id'] = command_id
        self._save(data=self.to_json())

    def save(self) -> None:
        """Сохраняет в БД текущие данные диалога.

        Raises:
            RuntimeError если диалог не открыт.
        """
        if not self.is_open():
            raise RuntimeError(f'Dialog for user "{self.user_id}" is not open')

        self.logger.info(f'Update dialog for user "{self.user_id}"')
        self._save(data=self.to_json())

    def to_json(self) -> str:
        """Преобразование диалога в формат Json.

        Returns:
            Json строка с данными диалога.
        """
        return json.dumps(self)

    def _initialize_data(self, data: Union[Dict[str, Any], str] = None) -> None:
        """Инициализирует данные диалога.

        Args:
            data: данные JSON подобного формата.

        Returns:
            ValueError если аргумента data имеет тип отличный от str, dict, None.
        """
        if data is None:
            data = json.loads(self._user.dialog_data or '{}')

        elif isinstance(data, str):
            data = json.loads(data)

        elif not isinstance(data, dict):
            raise ValueError(f'Expected dict or str, got {type(data)}')

        for key, value in data.items():
            self[key] = value

    def _save(self, data: str) -> None:
        """Сохраняет в БД переданные данные для диалога.

        Args:
            data: данные для сохранения.
        """
        self.logger.debug(f'Saving dialog data {data} for user "{self.user_id}"')

        self._user.dialog_data = data
        self._session.merge(self._user)
        self._session.commit()

    def __repr__(self):
        return f"{self.__class__}: {self.items()}"
