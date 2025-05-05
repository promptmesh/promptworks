from typing import Any, List, Optional
from promptworks import interfaces
from promptworks.components.chathistoryitem import ChatHistoryItem

class PromptHistory():
    """
    Represents a chat history in a conversation.
    
    Each chat history item can contain multiple components, which can be either text or other prompt components.
    """

    context: List[interfaces.BasePromptComponent]
    messages: List[interfaces.BasePromptComponent]

    def __init__(self, context: Optional[List[interfaces.BasePromptComponent]] = None) -> None:
        self.context = context.copy() if context else []
        self.messages = []

    def get_context(self) -> List[interfaces.BasePromptComponent]:
        """
        Get a copy of the context components.
        """
        return self.context.copy()
    
    def add_context(self, component: interfaces.BasePromptComponent) -> None:
        """
        Add a component to the context.
        """
        if not isinstance(component, interfaces.BasePromptComponent):
            raise TypeError(f"Expected a BasePromptComponent, got {type(component)}")
        self.context.append(component)

    def set_context(self, context: List[interfaces.BasePromptComponent]) -> None:
        """
        Set the context to a new list of components.
        """
        if not isinstance(context, list):
            raise TypeError(f"Expected a list, got {type(context)}")
        self.context = context.copy()

    def remove_context(self, component: interfaces.BasePromptComponent) -> None:
        """
        Remove a component from the context.
        """
        if component in self.context:
            self.context.remove(component)
        else:
            raise ValueError(f"Component {component} not found in context")
        
    def clear_context(self) -> None:
        """
        Clear all components from the context.
        """
        self.context.clear()

    def get_messages(self) -> List[interfaces.BasePromptComponent]:
        """
        Get a copy of the message components.
        """
        return self.messages.copy()
    
    def add_message(self, role: str, components: List[interfaces.BasePromptComponent]) -> None:
        """
        Add a message to the chat history.
        """
        if not isinstance(role, str):
            raise TypeError(f"Expected a string, got {type(role)}")
        if not isinstance(components, list):
            raise TypeError(f"Expected a list, got {type(components)}")
        
        self.messages.append(ChatHistoryItem(role, components))

    def remove_message(self, index: int) -> None:
        """
        Remove a message from the chat history by index.
        """
        if index < 0 or index >= len(self.messages):
            raise IndexError("Message index out of range")
        del self.messages[index]

    def clear_messages(self) -> None:
        """
        Clear all messages from the chat history.
        """
        self.messages.clear()

    async def refresh(self) -> None:
        """
        Refresh all components in the context and messages.
        """
        for component in self.context:
            if isinstance(component, interfaces.AsyncRefreshable):
                await component.refresh()
        for message in self.messages:
            if isinstance(message, interfaces.AsyncRefreshable):
                await message.refresh()

    def render(self, renderer: interfaces.BaseHistoryRenderer) -> Any:
        """
        Render the chat history using the specified renderer.
        
        Args:
            renderer (interfaces.BaseHistoryRenderer): The renderer to use.
        
        Returns:
            Any: The rendered output.
        """
        return renderer.render(self)