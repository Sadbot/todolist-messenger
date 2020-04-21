from typing import List, Tuple, Union

import sqlalchemy
from transliterate import get_translit_function

from todolist.models import User
from todolist.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    transliterate = get_translit_function('ru')

    def get_full_user_info(self, msg_user_id: Union[str, int], messenger_id: int) -> sqlalchemy.engine.result.RowProxy:
        statement = sqlalchemy.sql.text(
            """select mu.*
                from public.msg_user mu
                where mu.ext_id = :user_id and mu.messenger_type_id = :messenger_id""")

        return self.db.execute(
            statement, {'user_id': str(msg_user_id), 'messenger_id': str(messenger_id)}).fetchone()

    def get_active_users(self, messenger_id) -> List[sqlalchemy.engine.result.RowProxy]:
        statement = sqlalchemy.sql.text(
            """select mu.ext_id, u.id as user_id
                from public.msg_user mu
                left join dialog d on d.msg_user_id = mu.id
                left join public.user u on d.user_id = u.id
                where d.is_active = true and u.is_active = true and mu.messenger_id = :messenger_id""")

        return self.db.execute(statement, {'messenger_id': str(messenger_id)}).fetchall()

    def get_active_user_messengers_by_msg_id(self, msg_user_id: str) -> List[Tuple[str, int]]:
        """Получение списка активных мессенджеров пользователя.

        Args:
            msg_user_id: идентификатор пользователя в одном из мессенджеров.

        Returns:
            Список мессенджеров пользователя.
        """
        statement = sqlalchemy.sql.text(
            f'''select m.name, u_m.id
                from user_messenger as u_m
                join msg_user as ms_u on u_m.msg_user_id = ms_u.id
                join messenger as m on m.id = ms_u.messenger_id
                where u_m.is_active = true
                    and u_m.user_id in (select u_m.user_id
                                        from msg_user as ms_u
                                        join user_messenger as u_m on ms_u.id = u_m.msg_user_id
                                        where ms_u.ext_id = '{msg_user_id}')
            ''')

        return self.db.execute(statement).fetchall()
