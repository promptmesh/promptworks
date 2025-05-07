import asyncio
from PIL import Image
from promptworks.primatives import text, image, treenode
from promptworks.primatives.baseprimative import Primative
from promptworks.nodes.functionalcomponent import FunctionalComponent

async def evaluate_component(component):
    """
    Construnct the virtual tree
    """

    if isinstance(component, FunctionalComponent):
        # If the component is a functional component, call it and get the result
        component = await component()

    if isinstance(component, Primative):
        return component

    elif isinstance(component, tuple):
        return treenode(
            children=list(await asyncio.gather(*[evaluate_component(c) for c in component]))
        )
        
    elif isinstance(component, str):
        return text(text=component)
    
    elif isinstance(component, Image.Image):
        return image(image=component, alt_text="Image")

    elif isinstance(component, int):
        return text(text=str(component))
    
    elif isinstance(component, float):
        return text(text=str(component))
    
    elif isinstance(component, bool):
        return text(text=str(component))
    
    elif isinstance(component, list):
        return treenode(
            children=list(await asyncio.gather(*[evaluate_component(c) for c in component]))
        )
    
    elif isinstance(component, dict):
        return treenode(
            children=list(await asyncio.gather(*[evaluate_component(c) for c in component.values()]))
        )