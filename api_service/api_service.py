import os
from typing import Any, ClassVar
from base_model import WBBaseModel


class ApiService(WBBaseModel):
    API_ROOT: ClassVar[str] = "https://api.synopticdata.com/v2/"
    synoptic_api_key: str

    def model_post_init(self, __context: Any) -> None:
        if len(self.synoptic_api_key) == 42:
            return
        api_key = os.getenv("SYNOPTIC_API_KEY")
        if not api_key:
            api_key = ""
            while len(api_key) != 42:
                api_key = input("Api key not set. Please provide the key: ").strip()
        self.synoptic_api_key = api_key


    def test(self) -> str:
        self.LOGGER.info("ApiService test method called.")
        return "API Service is working!"