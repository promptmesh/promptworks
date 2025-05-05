from promptworks import PromptHistory, TimeComponent, PlaintextComponent
from promptworks.renderers import XMLRenderer, JSONRenderer
from asyncio import run

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

run(history.refresh())

print(history.render(XMLRenderer()))
print(f"\n\n{'-'*20}\n\n")
print(history.render(JSONRenderer()))
print(f"\n\n{'-'*20}\n\n")