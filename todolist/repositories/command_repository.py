from typing import Dict, List

import sqlalchemy

from todolist.models import Command, User
from todolist.repositories.base_repository import BaseRepository


class CommandRepository(BaseRepository):
    def get_available_dict(self) -> Dict[str, Command]:
        commands = self.db.query(Command).filter(Command.is_active == True).all()

        return {command.filename.lower(): command for command in commands}

    def get_active(self):
        statement = sqlalchemy.sql.text(
            """select c.name, c.filename 
                 from public.command c 
                where c.is_active = true 
             order by id"""
        )
        return self.db.execute(statement).fetchall()

    def find_by_name(self, command_name: str):
        statement = sqlalchemy.sql.text(
            """select c.name, c.filename 
                 from public.command c 
                where c.is_active = true
                  and lower(c.name) LIKE :name 
             order by id"""
        )
        return self.db.execute(statement, {'name': '%' + command_name + '%'}).fetchall()

    def get_commands_by_keywords(self, keywords: List[str]) -> sqlalchemy.engine.result.RowProxy:
        # todo пофиксить sql инъекции, хоть и слова приходят от морфера
        condition_keywords = [f'ck.keyword = \'{word}\'' for word in keywords]
        ck_keyword_condition = ' or '.join(condition_keywords)
        statement = sqlalchemy.sql.text(f'''select *
                                            from public.command c
                                            where c.is_active = true 
                                                and c.id in (
                                                    select t.command_id
                                                    from (
                                                        select ck.command_id, count(distinct ck."group") count,
                                                                max(count(distinct ck."group")) over () max_count
                                                        from public.command_nkeywords ck
                                                        where {ck_keyword_condition}
                                                        group by ck.command_id
                                                    ) t
                                            where t.count = t.max_count);''')
        return self.db.execute(statement).fetchall()
