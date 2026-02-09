from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class BaseConfig:
    sources: List[str]
    llm_type: str
    llm_config: dict