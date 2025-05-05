from asyncio import run

from dotenv import load_dotenv
from openai import OpenAI

from promptworks import PlaintextComponent, PromptHistory, TimeComponent
from promptworks.renderers import OpenAIChatRenderer

load_dotenv()

history = PromptHistory()

history.set_context([
    TimeComponent(),
    PlaintextComponent("system", "You are a helpful assistant.")
])
history.add_message("user", [
    PlaintextComponent("content", "Write a short haiku"),
])
history.add_message("assistant", [
    PlaintextComponent("content", "Wires hum in silence,\ncold logic shapes dawn's command—\nbits fall like spring rain.")
])
history.add_message("user", [
    PlaintextComponent("content", "Write another")
])

run(history.refresh())

messages = history.render(OpenAIChatRenderer())

print("[")
for message in messages:
    print(f"  {message},")
print("]")

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=messages
)

print(completion.choices[0].message.content)
