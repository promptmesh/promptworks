from promptworks.components.localfile import LocalFileComponent
from pathlib import Path

import pytest

@pytest.mark.asyncio
async def test_plaintext_component():
    component = LocalFileComponent(Path("README.md"))
    path = Path("README.md")
    assert component.path == path 

    # if you do not refresh the component, it should error when trying to serialize it
    with pytest.raises(RuntimeError):
        component.as_xml()

    with pytest.raises(RuntimeError):
        component.as_json()

    await component.refresh()

    assert component.text == path.read_text(encoding="utf-8")

    xml = component.as_xml()
    assert xml.tag == "file"
    assert xml.text == component.text
    assert xml.get("path") == str(path.absolute()) # type: ignore
    assert xml.get("mime-type").startswith("text/") # type: ignore

    json = component.as_json()
    assert json["type"] == "file"
    assert json["path"] == str(path.absolute()) # type: ignore
    assert json["mime-type"].startswith("text/") # type: ignore


@pytest.mark.parametrize("path", [
    Path("."),
    "fakepath",
    41,
    ]
)
def test_invalid_inputs(path):
    with pytest.raises((TypeError, ValueError)):
        LocalFileComponent(path)