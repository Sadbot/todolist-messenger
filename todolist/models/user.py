import bcrypt
import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer, Unicode
from sqlalchemy.sql import expression

from todolist.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=30))
    last_name = Column(Unicode(length=30))
    email = Column(Unicode(length=100))
    _password = Column('password', Unicode(length=60))

    creation_date = Column(DateTime(timezone=True), default=dt.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=dt.datetime.utcnow)

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
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_active': self.is_active
        }
