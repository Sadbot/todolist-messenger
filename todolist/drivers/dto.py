"""
Универсальные DTO объекты, которые хранят данные сообщения
пользователя вне зависимости от драйвера
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from todolist.components.builder import InteractiveComponentsBuilder

SLACK_MESSENGER = 1
TELEGRAM_MESSENGER = 2


@dataclass
class RequestMessage:
    user_id: str
    text: str  # текст пользовательского сообщения
    dialog_id: str  # ид диалога
    messenger_type: int
    command_name: Optional[str] = None  # название команды, если есть
    email: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    actions: Optional[List[Dict[str, Any]]] = None


@dataclass
class ResponseMessage:
    user_id: str
    command_name: str
    text: Optional[str] = None
    photo: Optional[bytes] = None
    interactive_components: Optional[InteractiveComponentsBuilder] = None
