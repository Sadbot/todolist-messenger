# Todolist-messenger

Universal chat-bot for slack\telegram with todolist/ 

## Project initialization

### Environment configuration
Перед запуском проекта нужно в корневой папке создать файл .env по примеру .env.example, заменив на свои значения

#### Рабочее окружение
Окружение определяется переменной `CURRENT_ENV`, которая может принимать одно из следующих значений:
- prod - окружение для запуска приложения на "боевом" сервере;
- dev - окружение для разработки. Отличается от prod окружения DEBUG уровнем логирования и поднятием БД на localhost вне зависимости от значения переменной `DB_HOST`;
- test - окружение для тестирования. Отличается от prod окружения использованием тестовой БД.

#### Токен для телеграм бота
Токен указать в файле .env для переменной TELEGRAM_TOKEN 

Для запуска приложения и бота необходимо выполнить команду:
```
docker-compose -f docker-compose.yml -f docker-compose-telegram.yaml up 
```

### Запуск в docker
```shell script
docker-compose  up --build
```

### Локальный запуск проекта
Для того, что бы запустить проект без docker, необходимо:

 - убедиться в том, что установлена необходимая версия `python=3.8`, и если нет - установить (`sudo apt-get install python3.8`)

 - далее устанавливаем пакетный менеджер `poetry` ([подробнее о модуле](https://python-poetry.org/))
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
   python3 get-poetry.py --version 1.0.2
   ```

 - установить зависимости из `pyproject.toml` (автоматически создается окружение для `poetry`, по умолчанию находится в `~/.cache/pypoetry/virtualenvs`)
    ```
    poetry install
    ```

 - запустить основные сервисы в `docker` (БД и другие сервисы) командой:
    
    ```shell script
    docker-compose up --build -d && docker-compose stop app && docker-compose stop telegram
    ```

 - запустить само приложение с указанием каких настроек хотим запустить
    > Запуск приложения необходимо выполнять только в активированном окружении.
    ```bash
    python3 main.py
    ```

 - !! Использовать python-линтер flake8 при разработки приложения. (есть поддержка в IDE или активация при гит-хуках)
    > Например, добавить pre-commit событие можно командой:
    ```bash
    $ flake8 --install-hook git
    $ git config --bool flake8.strict true
    ```

### Создание новых моделей и миграции
- при создании новой модели наследуем от Base-модели из `todolist/models/base.py`
- добавляем импорт созданной модели в `todolist/models/__init__.py`
- выполняем команду для создании миграции`alembic revision --autogenerate -m "your comment"`
- !!при создании foreignkey связей необходимо указывать название связи ForeignKey(...name='fk_...', ...) для того, чтобы миграция корректно могла откатываться. 
подробности: https://github.com/miguelgrinberg/Flask-Migrate/issues/155
и вот здесь: https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.create_foreign_key.params.name !!
- применяем миграцию `alembic upgrade head`
