import datetime as dt
import re

PATTERN_PRE_SNAKE = re.compile(r'(.)([A-Z][a-z]+)')
PATTERN_POST_SNAKE = re.compile(r'([a-z0-9])([A-Z])')


def to_snake_case(string: str) -> str:
    name = PATTERN_PRE_SNAKE.sub(r'\1_\2', string)
    return PATTERN_POST_SNAKE.sub(r'\1_\2', name).lower()
