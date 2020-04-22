import datetime as dt
import sqlalchemy

from todolist.models import Task
from todolist.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    def get_available(self, request_user_id: str):
        statement = sqlalchemy.sql.text(
            """select t.*
                 from public.task t
                 join msg_user mu on mu.id = t.msg_user_id 
                where mu.ext_id = :request_user_id 
             order by id"""
        )
        return self.db.execute(statement, {'request_user_id': request_user_id}).fetchall()

    def save_new(self, body: str, user_id: int) -> Task:
        new_task = Task(
            msg_user_id=user_id,
            text=body,
        )

        self.db.add(new_task)
        self.db.commit()

        return new_task

    def save_new(self, body: str, user_id: int) -> Task:
        new_task = Task(
            msg_user_id=user_id,
            text=body,
        )

        self.db.add(new_task)
        self.db.commit()

        return new_task
