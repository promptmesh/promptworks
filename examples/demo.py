from pathlib import Path
from promptworks import Prompt, LocalFileComponent, TimeComponent, PlaintextComponent
import asyncio

async def main():
    prompt = Prompt()
    prompt.add_component(LocalFileComponent(Path("README.md")))
    prompt.add_component(TimeComponent())
    prompt.add_component(PlaintextComponent("test", "Hello, world!"))

    await prompt.refresh()

    print(prompt.render_as_xml())
    print(f"\n\n{'-'*20}\n\n")
    print(prompt.render_as_json())

asyncio.run(main())