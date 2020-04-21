#!/bin/sh

alembic upgrade head

export PYTHONPATH=$PYTHONPATH:$PWD

python main.py