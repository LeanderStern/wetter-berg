import locale
import logging
import os

import discord
from dotenv import load_dotenv

load_dotenv(interpolate=True)
locale.setlocale(locale.LC_TIME, os.getenv("LOCAL"))

from discord_client.discord_client import DiscordClient

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    discord_client = DiscordClient(intents=intents)
    discord_client.run(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    main()