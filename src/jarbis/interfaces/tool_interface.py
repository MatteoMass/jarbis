from abc import ABC, abstractmethod
from typing import Any

class ToolInterface(ABC):
    
    @abstractmethod
    def tool_definition(self, *args, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def invoke(self, *args, **kwargs) -> Any:
        pass