import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BaseConfig:
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))
    CURRENT_ENV: str = os.environ.get('CURRENT_ENV', 'dev')
    LOCAL_MODE: bool = bool(int(os.environ.get('LOCAL_MODE', 1)))
    LOCAL_HOST: str = '127.0.0.1'
    HOST: str = os.getenv('HOST', LOCAL_HOST)
    PORT: int = int(os.getenv('PORT', 8080))

    TEMPLATES_DIR: str = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR: str = os.path.join(BASE_DIR, 'static')
    SECRET_KEY: str = os.getenv('SECRET_KEY')

    LOGGER_LEVEL = 'INFO'

    # app
    DEBUG = False
    TESTING = False

    # db
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
    SLACK_PORT = os.getenv('SLACK_PORT')

    TIMEZONE = 'Europe/Moscow'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return (
            f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


class DevConfig(BaseConfig):
    LOGGER_LEVEL = 'DEBUG'

    # app
    DEBUG = True
    TESTING = True

    @property
    def DB_HOST(self):
        return self.LOCAL_HOST if self.LOCAL_MODE else BaseConfig.DB_HOST


class TestConfig(DevConfig):
    LOGGER_LEVEL = 'INFO'

    @property
    def DB_NAME(self):
        return f'test_{DevConfig.DB_NAME}'


class ProdConfig(BaseConfig):
    pass


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}


def _get_config_gen():
    import sys
    sys.stderr.write(os.getenv('CURRENT_ENV', 'dev'))

    conf = config[os.getenv('CURRENT_ENV', 'dev')]()
    while True:
        yield conf


_config_gen = _get_config_gen()
next(_config_gen)


def get_config():
    return next(_config_gen)
