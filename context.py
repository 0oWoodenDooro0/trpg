import logging
import os
from datetime import datetime

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
ADMIN = os.getenv('ADMIN')
GUILD = discord.Object(id=GUILD_ID)

LOGGER = logging.getLogger("discord")
HANDLER = logging.FileHandler(filename=datetime.now().strftime("logs/%Y_%m_%d_%H_%M_%S.log"), encoding='utf-8',
                              mode='w')
datetime_formatter = "%Y-%m-%d %H:%M:%S"
FORMATTER = logging.Formatter(
    fmt="{asctime} | {levelname:<8} | {filename}:{funcName}:{lineno} - {message}",
    datefmt=datetime_formatter,
    style="{",
)
