from functools import cached_property
from logging import Logger
import logging
from typing import ClassVar
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class WBBaseModel(BaseModel):
    
    _LOGGER: ClassVar[Logger | None] = None

    @cached_property
    def logger(self) -> Logger:
        return logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")