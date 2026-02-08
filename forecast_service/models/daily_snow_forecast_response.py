from datetime import datetime

from base_model import WBBaseModel


class DailySnowForecastResponse(WBBaseModel):
    snowfall_sum: list[float]
    precipitation_probability_max: list[int]
    time: list[datetime]