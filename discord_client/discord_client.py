import datetime
import os

import discord
from discord.ext import tasks

from forecast_service.forecast_service import ForecastService

class DiscordClient(discord.Client):

    FORECAST_CHANNEL_ID: int = int(os.getenv("FORECAST_CHANNEL_ID"))
    FORECAST_MESSAGE_TIME: datetime.time = datetime.time(hour=int(os.getenv("FORECAST_MESSAGE_HOUR")),
                                                         tzinfo=datetime.datetime.now().astimezone().tzinfo)

    async def on_ready(self) -> None:
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def setup_hook(self) -> None:
        self.activity = discord.Game(name="Gilf Simulator")
        self.send_forecast_info_message.start()

    @tasks.loop(time=FORECAST_MESSAGE_TIME, reconnect=True)
    async def send_forecast_info_message(self) -> None:
        channel = self.get_channel(self.FORECAST_CHANNEL_ID)
        if not channel:
            raise ValueError("Channel not found")

        forecast_service = ForecastService()
        daily_forecast = forecast_service.get_daily_snow_forecast()
        hourly_forecast = forecast_service.get_hourly_snow_forecast()
        message = ""

        for i, daily_snowfall_sum in enumerate(daily_forecast.snowfall_sum):
            if daily_snowfall_sum > 0:
                loop_date = daily_forecast.time[i]
                snowfall_time_periods = hourly_forecast.get_snowfall_intervals(loop_date)

                snowfall_time_periods_string = ""
                if len(snowfall_time_periods) > 1:
                    for j, period in enumerate(snowfall_time_periods):
                        snowfall_time_periods_string += ("\n" if j == 0 else "") + ">   - " + str(period) + "\n"
                else:
                    snowfall_time_periods_string = snowfall_time_periods[0].time_range_str

                message += (f"## {"☃️" if daily_snowfall_sum > 3 else "⛄"} {loop_date.strftime("%A, %d.%m")}\n" +
                            f"> - **❄️ Aktuelle Schneehöhe:** {hourly_forecast.current_snow_depth}cm\n" +
                            f"> - **🌨️ Neuschnee:** {daily_snowfall_sum}cm\n" +
                            f"> - **🔮 Wahrscheinlichkeit:** {daily_forecast.precipitation_probability_max[i]}%\n" +
                            f"> - **🕑 Zeitraum:** " + snowfall_time_periods_string + "\n")
        if len(message) > 0:
            await channel.purge()
            await channel.send(message)
        else:
            print("No snowfall detected")

    @send_forecast_info_message.before_loop
    async def before_webhook_task(self):
        await self.wait_until_ready()