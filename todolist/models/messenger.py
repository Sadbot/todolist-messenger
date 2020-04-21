from sqlalchemy import Column, String, Integer, ForeignKey, JSON, UniqueConstraint

from todolist.models.base import Base


class MessengerType(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20))


class MsgUser(Base):
    __table_args__ = (
        UniqueConstraint('ext_id', 'messenger_type_id', name='_ext_id_messenger_id'),
    )
    id = Column(Integer, primary_key=True)
    ext_id = Column(String(length=100), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey(
            'user.id', name='fk_messenger_user_user_id',
            onupdate='CASCADE', ondelete='CASCADE'
        )
    )
    email = Column(String(length=100))
    username = Column(String(length=100))
    phone = Column(String(length=20))
    messenger_type_id = Column(Integer, nullable=False)
    dialog_data = Column(JSON)


class Dialog(Base):
    id = Column(Integer, primary_key=True)
    msg_user_id = Column(
        Integer,
        ForeignKey(
            'msg_user.id', name='fk_user_messenger_msg_user_id',
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=False
    )
    dialog_data = Column(JSON)
