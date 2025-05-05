from typing import List, Optional
from promptworks import interfaces
from promptworks.interfaces import BasePromptComponent
from lxml.etree import Element, _Element

class ChatHistoryItem(BasePromptComponent):
    """
    Represents a single chat message in a chat history.
    """

    role: str
    components: List[BasePromptComponent]

    def __init__(self, role: str, components: Optional[List[BasePromptComponent]] = None) -> None:
        self.role = role
        self.components = components.copy() if components else []

    async def refresh(self) -> None:
        """
        Refresh the components in the chat history item.
        """
        for component in self.components:
            if isinstance(component, interfaces.AsyncRefreshable):
                await component.refresh()

    def as_xml(self) -> _Element:
        el = Element(self.role)

        for component in self.components:
            el.append(component.as_xml())

        return el

    def as_json(self) -> dict:
        return {
            "type": "message",
            "role": self.role,
            "content": [component.as_json() for component in self.components]
        }
