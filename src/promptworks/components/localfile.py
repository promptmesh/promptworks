import pathlib
import mimetypes
from typing import Optional
from lxml.etree import Element, _Element
from promptworks.interfaces import BasePromptComponent  # Assuming valid import

class LocalFileComponent(BasePromptComponent):
    path: pathlib.Path
    text: Optional[str]

    def __init__(self, path: pathlib.Path) -> None:
        if not isinstance(path, pathlib.Path):
            raise TypeError(f"Expected a pathlib.Path object, got {type(path)}")
        if not path.is_file():
            raise ValueError(f"Provided path '{path}' is not a file.")
        self.path = path
        self.text = None

    async def refresh(self) -> None:
        self.text = self.path.read_text(encoding="utf-8")

    def _get_mime_type(self) -> str:
        mime, _ = mimetypes.guess_type(str(self.path))
        return mime or "text/plain"

    def as_xml(self) -> _Element:
        if self.text is None:
            raise RuntimeError("Component must be refreshed before serialization.")

        el = Element("file")
        el.text = self.text
        el.set("path", str(self.path.absolute()))
        el.set("mime-type", self._get_mime_type())
        return el

    def as_json(self) -> dict:
        if self.text is None:
            raise RuntimeError("Component must be refreshed before serialization.")

        return {
            "type": "file",
            "path": str(self.path.absolute()),
            "mime-type": self._get_mime_type(),
            "text": self.text
        }
