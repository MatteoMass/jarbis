from abc import ABC, abstractmethod
from typing import Iterator

class LLMInterface(ABC):
    
    @abstractmethod
    def generate(self, system_prompt: str, prompt: str, temperature: float) -> str:
        pass
    
    @abstractmethod
    def stream_generate(self, system_prompt: str, prompt: str, temperature: float) -> Iterator:
        pass