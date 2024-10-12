import random
import re

import discord
from discord import app_commands
from discord.ext import commands

from context import GUILD


class Dice:
    @staticmethod
    def roll(times: int, sided: int) -> int:
        return sum(random.randint(1, sided) for _ in range(times))


class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='roll')
    @app_commands.describe(dice='The dice you want to roll')
    async def roll(self, interaction: discord.Interaction, dice: str):
        match = re.match(r'(\d+)d(\d+)', dice, re.I)
        if match is None:
            await interaction.response.send_message("Please enter a valid dice pattern.", ephemeral=True,
                                                    delete_after=5)
            return
        times = int(match.group(1))
        sided = int(match.group(2))
        result = Dice.roll(times, sided)
        await interaction.response.send_message(f"You used {times} {sided}-sided dice.\nYou rolled a {result}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCog(bot), guild=GUILD)
    await bot.tree.sync(guild=GUILD)
