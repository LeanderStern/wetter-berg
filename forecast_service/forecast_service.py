import os
from datetime import datetime, timedelta
from functools import cached_property
from typing import Any, ClassVar

import requests
import requests_cache
import retry_requests
from pydantic import PrivateAttr
from requests import Response
from requests_cache import CachedSession

from forecast_service.enums.daily_weather_data_points_enum import DailyWeatherDataPointsEnum
from forecast_service.enums.hourly_weather_data_points_enum import HourlyWeatherDataPointsEnum
from base_model import WBBaseModel
from forecast_service.models.daily_snow_forecast_response import DailySnowForecastResponse

from forecast_service.models.hourly_snow_forecast_response import HourlySnowForecastResponse


class ForecastService(WBBaseModel):
    API_FORECAST_ROOT: ClassVar[str] = "https://api.open-meteo.com/v1/forecast"
    API_LOCATION_ARGUMENTS: ClassVar[dict[str, str]] = {"latitude": os.getenv("WEATHER_LATITUDE"),
                                                          "longitude": os.getenv("WEATHER_LONGITUDE")}
    API_TIME_ZONE: ClassVar[str] = os.getenv("TIME_ZONE")
    API_FORECAST_RANGE: ClassVar[str] = os.getenv("FORECAST_RANGE")

    _response: Response = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        cache_session: CachedSession = requests_cache.CachedSession('.cache', expire_after = 3600)
        session = retry_requests.retry(cache_session, retries = 5, backoff_factor = 0.2)
        today_date: datetime = datetime.now()

        self._response = session.get(url=self.API_FORECAST_ROOT, params={
            **self.API_LOCATION_ARGUMENTS,
            "hourly": [datapoint for datapoint in HourlyWeatherDataPointsEnum],
            "daily": [datapoint for datapoint in DailyWeatherDataPointsEnum],
            "timezone": self.API_TIME_ZONE,
            "start_date": today_date.strftime("%Y-%m-%d"),
            # minus one day because today is included in the forecast range
            "end_date": (today_date + timedelta(days = int(self.API_FORECAST_RANGE) - 1)).strftime("%Y-%m-%d")
        })
        self._response.raise_for_status()

    def get_hourly_snow_forecast(self) -> HourlySnowForecastResponse:
        hourly_response = self._response.json()["hourly"]
        return HourlySnowForecastResponse(**hourly_response)

    def get_daily_snow_forecast(self) -> DailySnowForecastResponse:
        daily_response = self._response.json()["daily"]
        return DailySnowForecastResponse(**daily_response)