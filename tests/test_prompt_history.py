from email import message
from promptworks import PromptHistory, TimeComponent, PlaintextComponent
from promptworks.renderers import XMLRenderer, JSONRenderer
import pytest


@pytest.mark.asyncio
async def test_prompt_history_render() -> None:
    history = PromptHistory()

    history.set_context([
        TimeComponent(),
        PlaintextComponent("system", "You are a helpful assistant.")
    ])
    history.add_message("user", [
        PlaintextComponent("content", "What is the weather like today?")
    ])
    history.add_message("assistant", [
        PlaintextComponent("content", "The weather is sunny today.")
    ])
    history.add_message("user", [
        PlaintextComponent("content", "Thank you!")
    ])

    await history.refresh()

    xml = history.render(XMLRenderer())
    assert xml is not None
    assert isinstance(xml, str)
    
    json = history.render(JSONRenderer())
    assert json is not None
    assert isinstance(json, str)

    json = history.render(JSONRenderer(pretty_print=False))
    assert json is not None
    assert isinstance(json, str)


@pytest.mark.asyncio
async def test_prompt_history_refresh() -> None:
    history = PromptHistory()

    history.set_context([
        TimeComponent(),
        PlaintextComponent("system", "You are a helpful assistant.")
    ])
    history.add_message("user", [
        TimeComponent(),
        PlaintextComponent("content", "What is the weather like today?")
    ])

    print(history.get_messages())
    await history.refresh()
    history.render(XMLRenderer())


def test_prompt_histoty_get_set_context() -> None:
    history = PromptHistory()
    time_component = TimeComponent()
    text_component = PlaintextComponent("system", "You are a helpful assistant.")
    history.set_context([time_component, text_component])
    assert history.get_context() == [time_component, text_component]

    history.remove_context(text_component)
    assert history.get_context() == [time_component]

    history.add_context(text_component)
    assert history.get_context() == [time_component, text_component]

    history.clear_context()
    assert history.get_context() == []

    with pytest.raises(ValueError):
        history.remove_context(time_component)

    with pytest.raises(TypeError):
        history.add_context(1) # type: ignore[arg-type]

    with pytest.raises(TypeError):
        history.set_context(1) # type: ignore[arg-type]

    with pytest.raises(ValueError):
        history.remove_context(1) # type: ignore[arg-type]


def test_prompt_history_get_set_messages() -> None:
    history = PromptHistory()
    time_component = TimeComponent()
    text_component = PlaintextComponent("system", "You are a helpful assistant.")

    history.add_message("user", [
        PlaintextComponent("content", "What is the weather like today?")
    ])
    assert len(history.get_messages()) == 1

    history.remove_message(0)
    assert len(history.get_messages()) == 0

    with pytest.raises(IndexError):
        history.remove_message(0)

    with pytest.raises(TypeError):
        history.add_message(1, [time_component]) # type: ignore[arg-type]

    with pytest.raises(TypeError):
        history.add_message("user", 1) # type: ignore[arg-type]

    with pytest.raises(IndexError):
        history.remove_message(1) # type: ignore[arg-type]

    assert len(history.get_messages()) == 0
    history.add_message("user", [text_component])
    assert len(history.get_messages()) == 1
    history.clear_messages()
    assert len(history.get_messages()) == 0


