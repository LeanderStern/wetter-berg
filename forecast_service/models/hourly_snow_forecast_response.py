from datetime import datetime
from functools import cached_property

from pydantic import validate_call

from base_model import WBBaseModel

from forecast_service.models.snowfall_hour_range import SnowfallTimeRange


class HourlySnowForecastResponse(WBBaseModel):
    time: list[datetime]
    snow_depth: list[float]
    snowfall: list[float]

    @validate_call
    def get_snowfall_intervals(self, date: datetime) -> list[SnowfallTimeRange]:
        """Returns snowfall time intervals. Only compares day and month."""
        start_time = None
        end_time = None
        snowfall_sum = 0
        time_ranges = []

        for time, snowfall in zip(self.time, self.snowfall):
            if time.day == date.day and time.month == date.month and snowfall > 0:
                snowfall_sum += snowfall
                if start_time is None:
                    start_time = time.time()
                    end_time = time.time()
                else:
                    end_time = time.time()
            elif start_time is not None:
                time_ranges.append(SnowfallTimeRange(start=start_time, end=end_time, snowfall_sum_cm=snowfall_sum))
                start_time = None
                end_time = None
                snowfall_sum = 0
        # only checks for start time because end time is always set when start time is
        if start_time is not None:
            time_ranges.append(SnowfallTimeRange(start=start_time, end=end_time, snowfall_sum_cm=snowfall_sum))
        return time_ranges

    @validate_call
    def get_snow_depth_diff(self, target_date: datetime) -> tuple[float, float]:
        """Returns snowfall time intervals. Only compares day and month."""
        depth_range = []
        for i, date in enumerate(self.time):
            if date.day == target_date.day and date.month == target_date.month:
                depth_range.append(self.snow_depth[i])
        return depth_range[0], depth_range[-1]
