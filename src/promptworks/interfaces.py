from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable
from lxml.etree import _Element

if TYPE_CHECKING: # pragma: no cover
    from promptworks.prompthistory import PromptHistory


@runtime_checkable
class BasePromptComponent(Protocol): # pragma: no cover
    """
    Interface for a prompt component.
    """

    def as_xml(self) -> _Element:
        """
        Convert the component to an XML string.

        This should be used to render the component as xml, do not fetch data or do computation here.
        """
        ...

    def as_json(self) -> dict:
        """
        Convert the component to a JSON string.

        This should be used to render the component as json, do not fetch data or do computation here.
        """
        ...

@runtime_checkable
class AsyncRefreshable(Protocol): # pragma: no cover
    """
    Interface for a component that can be refreshed asynchronously.
    """

    async def refresh(self) -> None:
        """
        Refresh the component.

        This will be called every time the component is rendered, and should be used to fetch the latest data.
        """
        ...

@runtime_checkable
class DynamicPromptComponent(BasePromptComponent, AsyncRefreshable, Protocol): # pragma: no cover
    """
    Interface for a dynamic prompt component.
    """
    ...


@runtime_checkable
class BaseHistoryRenderer(Protocol): # pragma: no cover
    """
    Interface for a history renderer.
    """

    def render(self, history: "PromptHistory") -> Any:
        """
        Render the chat history.

        This should be used to render the chat history as a string.
        """
        ...
