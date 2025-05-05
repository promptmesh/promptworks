from typing import Iterable, Optional, Sequence
from promptworks import interfaces
from lxml import etree
import json

class Prompt():
    _components: list[interfaces.BasePromptComponent]

    def __init__(self, components: Optional[list[interfaces.BasePromptComponent]] = None) -> None:
        self._components = components.copy() if components else []

    def add_component(self, component: interfaces.BasePromptComponent) -> None:
        """
        Add a component to the prompt.
        """
        if not isinstance(component, interfaces.BasePromptComponent):
            raise TypeError(f"Expected a BasePromptComponent, got {type(component)}")
        self._components.append(component)

    def remove_component(self, component: interfaces.BasePromptComponent) -> None:
        """
        Remove a component from the prompt.
        """
        if component in self._components:
            self._components.remove(component)
        else:
            raise ValueError(f"Component {component} not found in prompt")
        
    def clear(self) -> None:
        """
        Clear all components from the prompt.
        """
        self._components.clear()

    def __len__(self) -> int:
        """
        Get the number of components in the prompt.
        """
        return len(self._components)

    def __getitem__(self, index: int) -> interfaces.BasePromptComponent:
        """
        Get a component from the prompt by index.
        """
        return self._components[index]
    
    def __iter__(self) -> Iterable[interfaces.BasePromptComponent]: 
        """
        Iterate over the components in the prompt.
        """
        return iter(self._components)

    def get_components(self) -> Sequence[interfaces.BasePromptComponent]:
        """
        Get a copy of all components in the prompt.
        """
        return self._components.copy()

    async def refresh(self) -> None:
        for component in self._components:
            if isinstance(component, interfaces.AsyncRefreshable):
                await component.refresh()

    def render_as_xml(self) -> str:
        """
        Render the prompt as an XML string.
        """
        root = etree.Element("prompt")
        for component in self._components:
            root.append(component.as_xml())
        return etree.tostring(root, pretty_print=True).decode()
    
    def render_as_json(self) -> str:
        """
        Render the prompt as a JSON string.
        """
        prompt = list(map(lambda x: x.as_json(), self._components))
        return json.dumps(prompt, indent=4)