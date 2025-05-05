from promptworks import interfaces
from promptworks.prompthistory import PromptHistory
from lxml import etree
from lxml.etree import Element


class XMLRenderer(interfaces.BaseHistoryRenderer):
    """
    Renders the chat history as XML.
    """
    pretty_print: bool

    def __init__(self, pretty_print: bool = True) -> None:
        self.pretty_print = pretty_print

    def render(self, history: PromptHistory) -> str:
        """
        Render the chat history as XML.

        Args:
            history (PromptHistory): The chat history to render.

        Returns:
            str: The rendered XML string.
        """
        root = Element("chat_history")

        system_prompt = Element("system_prompt")
        for component in history.context:
            system_prompt.append(component.as_xml())

        root.append(system_prompt)

        conversation = Element("conversation")
        for item in history.messages:
            conversation.append(item.as_xml())

        root.append(conversation)

        return etree.tostring(root, pretty_print=self.pretty_print).decode()