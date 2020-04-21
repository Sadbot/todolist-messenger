"""
Модель для хранения настроек для команд чат-ботов
По каким параметрам обрабатывать команды и что выводить в мессенджер
"""

import datetime as dt

from sqlalchemy import Column, Unicode, Integer, DateTime, String, UnicodeText, Boolean, ForeignKey
from sqlalchemy.sql import expression
from todolist.models.base import Base


class Command(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), index=True, nullable=False)
    filename = Column(String(length=255))
    response_text = Column(UnicodeText)
    keywords1 = Column(Unicode)
    keywords2 = Column(Unicode)
    keywords3 = Column(Unicode)
    keywords4 = Column(Unicode)
    keywords5 = Column(Unicode)
    is_active = Column(
        Boolean, server_default=expression.true(), default=True,
        nullable=False
    )
    creation_date = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=dt.datetime.utcnow)


class CommandNkeywords(Base):
    id = Column(Integer, primary_key=True)
    keyword = Column(String(length=255), nullable=False)
    group = Column(Integer, nullable=False)
    command_id = Column(
        Integer,
        ForeignKey(
            'command.id', name='fk_command_nkeywords_command_id_command_id',
            onupdate='CASCADE', ondelete='CASCADE'
        ), nullable=False
    )
