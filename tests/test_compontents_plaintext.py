import pytest
from promptworks.components.plaintext import PlaintextComponent


def test_plaintext_component():
    component = PlaintextComponent("test", "Hello, world!")
    assert component.name == "test"
    assert component.text == "Hello, world!"

    xml = component.as_xml()
    assert xml.tag == "test"
    assert xml.text == "Hello, world!"

    json = component.as_json()
    assert json["type"] == "plaintext"
    assert json["name"] == "test"
    assert json["text"] == "Hello, world!"


def test_invalid_name():
    with pytest.raises(ValueError):
        PlaintextComponent("123tag", "Hello, world!")