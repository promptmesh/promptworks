from pathlib import Path
from typing import List
import pytest
from promptworks import interfaces
from promptworks.components.localfile import LocalFileComponent
from promptworks.prompt import Prompt
from promptworks.components.plaintext import PlaintextComponent

def test_prompt() -> None:
    prompt = Prompt()
    assert len(prompt) == 0

    component = PlaintextComponent("test", "Hello, world!")

    prompt.add_component(component)
    assert len(prompt) == 1
    assert prompt[0] is component
    assert prompt[0].name == "test" # type: ignore
    assert prompt[0].text == "Hello, world!" # type: ignore

    prompt.remove_component(component)
    assert len(prompt) == 0

    prompt.clear()
    assert len(prompt) == 0

    with pytest.raises(TypeError):
        prompt.add_component("not a component") # type: ignore

    with pytest.raises(ValueError):
        prompt.remove_component(component)

    with pytest.raises(ValueError):
        prompt.remove_component(PlaintextComponent("test", "Hello, world!"))


def test_prompt_iter() -> None:
    components: List[interfaces.BasePromptComponent] = [
        PlaintextComponent("test", "Hello, world!"),
        PlaintextComponent("test2", "Hello, world!"),
        PlaintextComponent("test3", "Hello, world!"),
    ]
    prompt = Prompt(components)
    assert len(prompt) == 3

    for item in iter(prompt):
        assert isinstance(item, interfaces.BasePromptComponent)
        assert item in components


def test_prompt_json() -> None:
    components: List[interfaces.BasePromptComponent] = [
        PlaintextComponent("test", "Hello, world!"),
        PlaintextComponent("test2", "Hello, world!"),
        PlaintextComponent("test3", "Hello, world!"),
    ]
    prompt = Prompt(components)
    assert len(prompt) == 3

    json_data = prompt.render_as_json()
    assert isinstance(json_data, str)
    print(json_data)


def test_prompt_xml() -> None:
    components: List[interfaces.BasePromptComponent] = [
        PlaintextComponent("test", "Hello, world!"),
        PlaintextComponent("test2", "Hello, world!"),
        PlaintextComponent("test3", "Hello, world!"),
    ]
    prompt = Prompt(components)
    assert len(prompt) == 3

    xml_data = prompt.render_as_xml()
    assert isinstance(xml_data, str)
    print(xml_data)


@pytest.mark.asyncio
async def test_prompt_refresh() -> None:
    components: List[interfaces.BasePromptComponent] = [
        LocalFileComponent(Path("README.md")),
    ]
    prompt = Prompt(components)
    assert len(prompt) == 1

    await prompt.refresh()

    xml = prompt.render_as_xml()
    assert "<file" in xml
    assert "</file>" in xml



def test_prompt_get_components() -> None:
    components: List[interfaces.BasePromptComponent] = [
        PlaintextComponent("test", "Hello, world!"),
        PlaintextComponent("test2", "Hello, world!"),
        PlaintextComponent("test3", "Hello, world!"),
    ]
    prompt = Prompt(components)
    assert len(prompt) == 3

    retrieved_components = prompt.get_components()
    assert len(retrieved_components) == 3
    for component in retrieved_components:
        assert isinstance(component, interfaces.BasePromptComponent)