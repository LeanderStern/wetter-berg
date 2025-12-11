from logging import Logger
import logging
from typing import Any, ClassVar
from pydantic import BaseModel


class WBBaseModel(BaseModel):
    LOGGER: ClassVar[Logger] = logging.getLogger(__name__)

    def model_post_init(self, __context: Any) -> None:
        logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
)