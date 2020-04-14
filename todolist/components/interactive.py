from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Option:
    text: str
    value: str


@dataclass
class Link:
    text: str
    link: str


@dataclass
class Button:
    id: str
    value: str
    text: str
    label: Optional[str]


@dataclass
class DatetimePicker:
    id: str
    since: Optional[datetime]
    until: Optional[datetime]
    label: Optional[str]


@dataclass
class Select:
    id: str
    placeholder: str
    options: List[Option]
    initial: Optional[Option]
    label: Optional[str]


@dataclass
class MultiSelect:
    id: str
    placeholder: str
    options: List[Option]
    label: Optional[str]


@dataclass
class Checkbox:
    id: str
    options: List[Option]
    label: Optional[str]
