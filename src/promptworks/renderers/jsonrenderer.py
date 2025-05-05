from promptworks import interfaces
from promptworks.prompthistory import PromptHistory
import json


class JSONRenderer(interfaces.BaseHistoryRenderer):
    """
    Renders the chat history as XML.
    """
    pretty_print: bool
    indent: int = 4

    def __init__(self, pretty_print: bool = True) -> None:
        self.pretty_print = pretty_print

    def render(self, history: PromptHistory) -> str:
        """
        Render the chat history as JSON.

        Args:
            history (PromptHistory): The chat history to render.

        Returns:
            str: The rendered JSON string.
        """

        root = {
            "system_prompt": [x.as_json() for x in history.context],
            "conversation": [x.as_json() for x in history.messages]
        }

        if not self.pretty_print:
            return json.dumps(root)

        return json.dumps(root, indent=self.indent)