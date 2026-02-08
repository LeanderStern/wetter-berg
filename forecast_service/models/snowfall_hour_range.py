from datetime import time
from functools import cached_property
from typing import ClassVar

from base_model import WBBaseModel


class SnowfallTimeRange(WBBaseModel):
    TIME_FORMAT: ClassVar[str] = "%H:%M"

    start: time
    end: time
    snowfall_sum_cm: float

    def __str__(self):
        return f"{self.time_range_str}: {round(self.snowfall_sum_cm, 2)}cm"

    @cached_property
    def time_range_str(self):
        return f"{self.start.strftime(self.TIME_FORMAT)} - {self.end.strftime(self.TIME_FORMAT)}"