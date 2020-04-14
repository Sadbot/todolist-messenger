from typing import List, Tuple, Union

import sqlalchemy
from transliterate import get_translit_function

from todolist.models import User
from todolist.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    transliterate = get_translit_function('ru')

    def save_list(self, users: List[User]):
        self.db.bulk_save_objects(users)
        self.db.commit()

    def get_full_user_info(self, msg_user_id: Union[str, int], messenger_id: int) -> sqlalchemy.engine.result.RowProxy:
        statement = sqlalchemy.sql.text(
            """select mu.*, um.is_active is_um_active, u.is_active is_user_active
                from public.msg_user mu
                left join user_messenger um on um.msg_user_id = mu.id
                left join public.user u on um.user_id = u.id
                where mu.ext_id = :user_id and mu.messenger_id = :messenger_id""")

        return self.db.execute(
            statement, {'user_id': str(msg_user_id), 'messenger_id': str(messenger_id)}).fetchone()

    def get_active_users(self, messenger_id) -> List[sqlalchemy.engine.result.RowProxy]:
        statement = sqlalchemy.sql.text(
            """select mu.ext_id, u.id as user_id
                from public.msg_user mu
                left join user_messenger um on um.msg_user_id = mu.id
                left join public.user u on um.user_id = u.id
                where um.is_active = true and u.is_active = true and mu.messenger_id = :messenger_id""")

        return self.db.execute(statement, {'messenger_id': str(messenger_id)}).fetchall()

    def get_by_normalized(self, name_normal: str = None, surname_normal: str = None) -> sqlalchemy.engine.result.RowProxy:
        """Получение списка пользователей по нормализованному
        имени и / или фамилии"""
        if not name_normal and not surname_normal:
            raise ValueError('One of the parameters should be set: "name_normal" or "surname_normal"')

        if name_normal:
            name_normal = self.transliterate(name_normal, reversed=True).replace('\'', '')
        if surname_normal:
            surname_normal = self.transliterate(surname_normal, reversed=True).replace('\'', '')

        self.logger.info(f'trying to find user with normal_name={name_normal}, surname_normal={surname_normal}')

        statement = sqlalchemy.sql.text(
            """select *
                from public.user u
                where u.is_active = true
                        and (:surname_normal is null or u.last_name_normal = :surname_normal)
                        and (:name_normal is null or u.first_name_normal = :name_normal)""")

        return self.db \
            .execute(statement, {'surname_normal': surname_normal, 'name_normal': name_normal}) \
            .fetchall()

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
