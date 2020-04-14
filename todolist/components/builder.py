"""
Строитель интерактивных компонентов сообщения.

Пример использования:

handlers/common.py
    from todolist.components.interactive import Option
    from todolist.components.builder import InteractiveComponentsBuilder
    from todolist.drivers.dto import ResponseMessage

    def get_response_message():
        checkbox_options = [
                               Option(label='Option 1', value='first'),
                               Option(label='Option 2', value='second')
                            ]
        components = InteractiveComponentsBuilder().add_checkbox('id', checkbox_options).add_button('id', 'Text')

        return ResponseMessage(
            user_id=request.user_id,
            command_name='echo',
            text=request.text,
            photo=None,
            interactive_components: components
        )

drivers/bot/handlers.py
    ...
    response_message = get_response_message()
    for component in response_message.interactive_components:
        ...
"""
from collections import deque
from datetime import datetime
from typing import List

from todolist.components import interactive, simple


class InteractiveComponentsBuilder(deque):

    def add_datetime_picker(self, element_id: str, since: datetime = None, until: datetime = None,
                            label: str = None) -> 'InteractiveComponentsBuilder':
        self.append(
            interactive.DatetimePicker(id=element_id, since=since, until=until, label=label)
        )
        return self

    def add_select(self, element_id: str, placeholder: str, options: List[interactive.Option],
                   initial: interactive.Option = None, label: str = None) -> 'InteractiveComponentsBuilder':
        self.append(
            interactive.Select(id=element_id, placeholder=placeholder, options=options, initial=initial, label=label)
        )
        return self

    def add_multi_select(self, element_id: str, placeholder: str, options: List[interactive.Option],
                         label: str = None) -> 'InteractiveComponentsBuilder':
        self.append(
            interactive.MultiSelect(id=element_id, placeholder=placeholder, options=options, label=label)
        )
        return self

    def add_button(self, element_id: str, value: str, text: str, label: str = None) -> 'InteractiveComponentsBuilder':
        self.append(
            interactive.Button(id=element_id, value=value, text=text, label=label)
        )
        return self

    def add_checkbox(self, element_id: str, options: List[interactive.Option],
                     label: str) -> 'InteractiveComponentsBuilder':
        self.append(
            interactive.Checkbox(id=element_id, options=options, label=label)
        )
        return self

    def add_text(self, text: str) -> 'InteractiveComponentsBuilder':
        self.append(simple.Text(text=text))
        return self
