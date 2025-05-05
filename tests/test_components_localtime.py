import pytest
from promptworks.components.localtime import TimeComponent


@pytest.mark.asyncio
async def test_time_component_localtime():
    component = TimeComponent()
    assert component.timestamp is None
    assert component.timezone == "local"

    # cannot serialize before refresh
    with pytest.raises(RuntimeError):
        component.as_xml()

    with pytest.raises(RuntimeError):
        component.as_json()

    await component.refresh()

    assert component.timestamp is not None
    
    xml = component.as_xml()
    assert xml.tag == "time"
    assert xml.text == component.timestamp.isoformat()
    assert xml.get("format") == "YYYY-MM-DDTHH:MM:SS±HH:MM"
    assert xml.get("timezone") == "local"

    json = component.as_json()
    assert json["type"] == "time"
    assert json["timestamp"] == component.timestamp.isoformat()
    assert json["format"] == "YYYY-MM-DDTHH:MM:SS±HH:MM"
    assert json["timezone"] == "local"


@pytest.mark.asyncio
async def test_time_component_utc():
    component = TimeComponent(timezone="UTC")
    assert component.timestamp is None
    assert component.timezone == "UTC"

    # cannot serialize before refresh
    with pytest.raises(RuntimeError):
        component.as_xml()

    with pytest.raises(RuntimeError):
        component.as_json()

    await component.refresh()

    assert component.timestamp is not None
    
    xml = component.as_xml()
    assert xml.tag == "time"
    assert xml.text == component.timestamp.isoformat()
    assert xml.get("format") == "YYYY-MM-DDTHH:MM:SS±HH:MM"
    assert xml.get("timezone") == "UTC"

    json = component.as_json()
    assert json["type"] == "time"
    assert json["timestamp"] == component.timestamp.isoformat()
    assert json["format"] == "YYYY-MM-DDTHH:MM:SS±HH:MM"
    assert json["timezone"] == "UTC"


def test_invalid_timezone():
    with pytest.raises(ValueError):
        TimeComponent(timezone="invalid/timezone")