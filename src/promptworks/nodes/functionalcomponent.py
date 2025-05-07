from functools import wraps
from typing import Any, Callable, Coroutine, TypeAlias, Union
from .basecomponent import BaseComponent
import asyncio

FunctionType: TypeAlias = Callable[..., Union[Any, Coroutine[Any, Any, Any]]]

class FunctionalComponent(BaseComponent):
    function: FunctionType

    def __init__(self, function: FunctionType) -> None:
        self.function = function

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        try:
            result = self.function(*args, **kwds)

            # if async
            if asyncio.iscoroutine(result):
                return await result
            
            # if sync
            else : 
                return result
        
        except Exception as e:
            print(f"Error in FunctionalComponent: {str(e)}")
            raise e


def fc(function: FunctionType):
    """
    Decorator that converts a function (sync or async) into a FunctionalComponent.
    """
    @wraps(function)
    def wrapper(*args: Any, **kwds: Any) -> FunctionalComponent:
        return FunctionalComponent(function)
    
    return wrapper
