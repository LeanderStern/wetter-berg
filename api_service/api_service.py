import os
from typing import Any, ClassVar

from pydantic import validate_call
import requests
from base_model import WBBaseModel


class ApiService(WBBaseModel):
    API_ROOT: ClassVar[str] = "https://api.synopticdata.com/v2/"
    API_TOKEN_ENV_VAR: ClassVar[str] = "SYNOPTIC_API_TOKEN"
    SYNOPTIC_API_TOKEN_LENGTH: ClassVar[int] = 32

    _synoptic_api_token: str = ""
    _api_arguments: dict[str, str] = {}

    def model_post_init(self, __context: Any) -> None:
        api_token = os.getenv(ApiService.API_TOKEN_ENV_VAR)
        if not api_token or len(api_token) != ApiService.SYNOPTIC_API_TOKEN_LENGTH:
            self.LOGGER.warning(
                f"Invalid or missing {ApiService.API_TOKEN_ENV_VAR} environment variable."
            )
            while len(self._synoptic_api_token) != ApiService.SYNOPTIC_API_TOKEN_LENGTH:
                self._synoptic_api_token = input("Please provide a valid api token: ").strip()
            self.create_env_file(self._synoptic_api_token)
        else:
            self._synoptic_api_token = api_token
        
        self._api_arguments = {"token": self._synoptic_api_token, "stid": "KLAX"}

    def get_snow_forecast(self) -> requests.Response:
        return requests.get(f"https://api.synopticdata.com/v2/stations/timeseries?stid=mtmet,nahu&token=48e002e63eb648b583745ee6875a38d3&recent=120")
        
    
    @staticmethod
    @validate_call
    def create_env_file(api_token: str) -> None:
        ApiService.LOGGER.info("Creating .env file with provided API token.")
        with open(".env", "w") as f:
            f.write(f"{ApiService.API_TOKEN_ENV_VAR}={api_token}\n")