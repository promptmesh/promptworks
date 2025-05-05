from typing import List
from promptworks import interfaces
from promptworks import PromptHistory
from promptworks.components.chathistoryitem import ChatHistoryItem
from lxml import etree
from lxml.etree import Element

class OpenAIChatRenderer(interfaces.BaseHistoryRenderer):
    """
    Render the chat history in the OpenAI chat format.
    """

    def __init__(self) -> None:
        pass

    def render(self, history: PromptHistory) -> List[dict]:
        messages: List[dict] = []

        text = ""
        for component in history.context:
            text += f"  {component.as_text()}\n\n"

        system_prompt = {
            "role": "system",
            "content": text.strip()
        }

        messages.append(system_prompt)

        for msg in history.messages:
            assert isinstance(msg, ChatHistoryItem), "Expected ChatHistoryItem"
            text = msg.as_text()
            message = {
                "role": msg.role,
                "content": text.strip()
            }
            messages.append(message)

        return messages
