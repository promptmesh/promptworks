from promptworks.primatives.baseprimative import Primative
from promptworks.renderer.base import BaseRenderer, State
from promptworks.primatives import text, image, treenode

class TreeRenderer(BaseRenderer):

    def render(self, tree: Primative | None, state: State) -> str:

        def _render(node):
            if isinstance(node, text):
                return f"{node.text}\n"
            elif isinstance(node, image):
                return f"Image: {node.alt_text}\n"
            elif isinstance(node, treenode):
                output = "Children:\n"
                for child in node.children:
                    output += _render(child)
                return output
            return ""

        output = _render(tree)
        return output.strip()
