from datetime import datetime
from zoneinfo import ZoneInfo
from lxml.etree import Element, _Element
from typing import Optional
from promptworks.interfaces import BasePromptComponent

class TimeComponent(BasePromptComponent):
    timestamp: Optional[datetime]
    _format_string: str = "YYYY-MM-DDTHH:MM:SS±HH:MM"
    timezone: str

    def __init__(self, timezone: str = "local") -> None:
        if timezone != "local":
            try:
                ZoneInfo(timezone)  # validate
            except Exception:
                raise ValueError(f"Invalid timezone identifier: '{timezone}'")
        self.timezone = timezone
        self.timestamp = None

    async def refresh(self) -> None:
        if self.timezone == "local":
            self.timestamp = datetime.now().astimezone()  # system local with offset
        else:
            self.timestamp = datetime.now(ZoneInfo(self.timezone))

    def as_xml(self) -> _Element:
        if self.timestamp is None:
            raise RuntimeError("Component must be refreshed before serialization.")

        el = Element("time")
        el.text = self.timestamp.isoformat()
        el.set("format", self._format_string)
        el.set("timezone", self.timezone)
        return el

    def as_json(self) -> dict:
        if self.timestamp is None:
            raise RuntimeError("Component must be refreshed before serialization.")

        return {
            "type": "time",
            "timestamp": self.timestamp.isoformat(),
            "format": self._format_string,
            "timezone": self.timezone
        }
