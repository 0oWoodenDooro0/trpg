import discord
from discord import app_commands
from discord.ext import commands

from context import GUILD


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='player')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test", ephemeral=True, delete_after=3)


async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot), guild=GUILD)
    await bot.tree.sync(guild=GUILD)
