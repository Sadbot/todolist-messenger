FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ARG CURRENT_ENV=${CURRENT_ENV}

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -o ./get-poetry.py &&\
    python3 ./get-poetry.py --version 1.0.2 && rm ./get-poetry.py &&\
    ln -s /root/.poetry/bin/poetry /usr/bin/poetry && poetry config virtualenvs.create false

# Install ldap and cron
RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev cron

WORKDIR /app/

# Install dependences
COPY pyproject.toml poetry.lock /app/
RUN poetry install $(test "$CURRENT_ENV" == prod && echo "--no-dev") --no-interaction --no-ansi

COPY . /app/
