from promptworks.interfaces import BasePromptComponent
from lxml.etree import Element, _Element
import re

class PlaintextComponent(BasePromptComponent):
    def __init__(self, name: str, text: str) -> None:
        if not re.match(r'^[a-zA-Z_][\w\-\.]*$', name):
            raise ValueError(f"Invalid XML tag name: {name}")
        self.name = name
        self.text = text

    def as_xml(self) -> _Element:
        el = Element(self.name)
        el.text = self.text
        return el

    def as_json(self) -> dict:
        return {
            "type": "plaintext",
            "name": self.name,
            "text": self.text
        }
