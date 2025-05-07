from promptworks import fc, evaluate_component, TreeRenderer, RenderState
from asyncio import run

@fc
def hello():
    return "Hello, world!"

@fc
def love():
    return "I love ai!"

@fc
def hello_ai():
    return (
        hello(),
        love()
    )

tree = run(evaluate_component(hello_ai()))
print(TreeRenderer().render(tree, RenderState()))