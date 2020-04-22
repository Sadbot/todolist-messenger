import datetime as dt

from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime

from todolist.models.base import Base


class Task(Base):
    id = Column(Integer, primary_key=True)
    msg_user_id = Column(
        Integer,
        ForeignKey(
            'msg_user.id', name='fk_msg_user_id_msg_user_id',
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=False
    )
    text = Column(Text, nullable=False)
    use_date = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    parent_task_id = Column(
        Integer,
        ForeignKey(
            'task.id', name='fk_parent_id_task_id',
            onupdate='CASCADE', ondelete='CASCADE'
        )
    )

    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=dt.datetime.utcnow)
