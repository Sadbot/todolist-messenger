from sqlalchemy.ext.declarative import as_declarative, declared_attr
from todolist.utils.string_manipulation import to_snake_case


@as_declarative()
class Base(object):
    def __init__(self, *args, **kwargs):
        pass

    @declared_attr
    def __tablename__(cls):
        return to_snake_case(cls.__name__)
