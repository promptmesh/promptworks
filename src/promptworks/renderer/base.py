from typing import Any, Protocol

from promptworks.primatives.baseprimative import Primative

class State:
    model: str | None
    supports_image: bool = False


class BaseRenderer(Protocol):
    def render(self, tree: Primative, state: State) -> Any:
        """
        Render the tree
        """
        ...
