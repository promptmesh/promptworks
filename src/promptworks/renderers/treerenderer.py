from promptworks import interfaces
from promptworks.components.chathistoryitem import ChatHistoryItem
from promptworks.prompthistory import PromptHistory


class TreeRenderer(interfaces.BaseHistoryRenderer):
    """
    Renders the chat history in a tree-like format, similar to the UNIX `tree` command.
    """

    def render(self, history: PromptHistory) -> str:
        lines = []

        def format_component(component):
            data = component.as_json()
            typename = data.get("type", "unknown")
            label = data.get("name", data.get("role", data.get("path", "")))
            return f"{typename}: {label}".strip()

        def walk(name, children, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{name}")

            next_prefix = prefix + ("    " if is_last else "│   ")
            for i, comp in enumerate(children):
                last = i == len(children) - 1
                comp_line = format_component(comp)
                lines.append(f"{next_prefix}{'└── ' if last else '├── '}{comp_line}")

                if isinstance(comp, interfaces.HasChildNodes):
                    sub_children = comp.get_child_nodes()
                    if sub_children:
                        walk_children(sub_children, next_prefix + ("    " if last else "│   "))

        def walk_children(components, prefix):
            for i, comp in enumerate(components):
                is_last = i == len(components) - 1
                line = format_component(comp)
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}{line}")

                if hasattr(comp, "get_child_nodes"):
                    sub = comp.get_child_nodes()
                    if sub:
                        walk_children(sub, prefix + ("    " if is_last else "│   "))

        # Root
        lines.append("root")

        # system_prompt
        walk("system_prompt", history.context, prefix="", is_last=False)

        # conversation
        conv_prefix = "│   " if history.context else ""
        lines.append(f"{'└── ' if not history.context else '├── '}conversation")

        for i, msg in enumerate(history.messages):
            assert isinstance(msg, ChatHistoryItem), "Expected ChatHistoryItem"
            is_last_msg = i == len(history.messages) - 1
            branch = "└── " if is_last_msg else "├── "
            lines.append(f"{conv_prefix}{branch}message: {msg.role}")
            if isinstance(msg, interfaces.HasChildNodes):
                children = msg.get_child_nodes()
                walk_children(children, conv_prefix + ("    " if is_last_msg else "│   "))

        return "\n".join(lines)
