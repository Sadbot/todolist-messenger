import datetime as dt

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import expression
from todolist.models.base import Base


class Messenger(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20))


class UserMessenger(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey('user.id', name='fk_user_messenger_user_id_user_id', ondelete='CASCADE'),
        nullable=False
    )

    msg_user_id = Column(Integer,
                         ForeignKey(
                             'msg_user.id', name='fk_user_messenger_msg_user_id',
                             onupdate='CASCADE', ondelete='CASCADE'
                         ),
                         nullable=False)
    is_active = Column(
        Boolean, server_default=expression.true(), default=True,
        nullable=False
    )
    is_default = Column(
        Boolean, server_default=expression.false(), default=False,
        nullable=False
    )

    creation_date = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=dt.datetime.utcnow)
