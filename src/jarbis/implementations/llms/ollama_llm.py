from typing import Iterator
import ollama
from jarbis.interfaces.llm_interface import LLMInterface


class OllamaLLM(LLMInterface):
    def __init__(self, config: dict):
        endpoint = config.get("endpoint", "http://localhost:11434")
        self.model_name = config.get("model_name")
        
        self.client = ollama.Client(host=endpoint)

    def _build_messages(self, system_prompt: str, prompt: str) -> list:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

    def generate(self, system_prompt: str, prompt: str, temperature: float) -> str:
        messages = self._build_messages(system_prompt, prompt)
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options={"temperature": temperature},
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Errore nella chiamata a Ollama: {e}")

    def stream_generate(
        self, system_prompt: str, prompt: str, temperature: float
    ) -> Iterator[str]:
        messages = self._build_messages(system_prompt, prompt)
        
        try:
            stream = self.client.chat(
                model=self.model_name,
                messages=messages,
                options={"temperature": temperature},
                stream=True
            )
            
            # Itera sui chunk dello stream
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            raise Exception(f"Errore nello streaming da Ollama: {e}")