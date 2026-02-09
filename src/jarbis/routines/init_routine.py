from jarbis.config import BaseConfig
from jarbis.connectors.obsidian_connector import obsidian_connector
import json


def init_routine() -> BaseConfig:
    main_file = "__init__.md"

    content = obsidian_connector.get_page_content(main_file)
    return BaseConfig(**json.loads(content))
