import bcrypt
import datetime as dt
import enum

from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey, JSON, String, Unicode, UniqueConstraint, Index
from sqlalchemy.sql import expression
from todolist.models.base import Base


class AvailableRoles(enum.Enum):
    ADMIN: str = 'admin'
    MANAGER: str = 'manager'
    USER: str = 'user'


# TODO todolist-62 create seeds for roles
class Role(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(length=30))


class MsgUser(Base):
    __table_args__ = (
        UniqueConstraint('ext_id', 'messenger_id', name='_ext_id_messenger_id'),
    )
    id = Column(Integer, primary_key=True)
    email = Column(String(length=100))
    username = Column(String(length=100))
    ext_id = Column(String(length=100), nullable=False)
    phone = Column(String(length=20))
    messenger_id = Column(Integer, nullable=False)
    dialog_data = Column(JSON)


class User(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=30))
    last_name = Column(Unicode(length=30))
    first_name_normal = Column(String(length=40), index=True)
    last_name_normal = Column(String(length=40), index=True)
    ldap_username = Column(String(length=100), unique=True, nullable=False)
    email = Column(Unicode(length=100))
    _password = Column('password', Unicode(length=60))
    group = Column(String(length=50))
    role = Column(Integer, ForeignKey('role.id', name='fk_user_role_role_id', onupdate='CASCADE', ondelete='CASCADE'))
    is_active = Column(
        Boolean, server_default=expression.false(), default=False,
        nullable=False
    )

    creation_date = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=dt.datetime.utcnow)

    __table_args__ = (Index('normalized_names', 'last_name_normal', 'first_name_normal'),)

    def __str__(self):
        return f'<User id={self.id} ldap_username={self.ldap_username} ' \
               f'role={self.role} is_active={self.is_active}>'

    @property
    def password(self):
        return self._password

    @staticmethod
    def generate_password(raw_password: str):
        return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, inp_passwd: str):
        return bcrypt.checkpw(inp_passwd.encode(), self.password.encode())

    def to_json(self):
        return {
            'id': self.id,
            'nick': self.nick,
            'email': self.email,
            'is_active': self.is_active
        }
