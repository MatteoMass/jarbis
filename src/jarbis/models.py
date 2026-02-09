from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedditSourceModel:
    title: str
    text: str