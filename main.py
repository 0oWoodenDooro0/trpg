import discord
from discord.ext import commands

from context import TOKEN, FORMATTER, HANDLER


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.tree.sync()


bot = MyBot()


@bot.event
async def on_ready():
    print("bot is ready.")


@bot.tree.command()
async def load(interaction: discord.Interaction, extension: str):
    await bot.load_extension(f"cogs.{extension}")
    await interaction.response.send_message("Load Successfully!", ephemeral=True, delete_after=3)
    await bot.tree.sync()


@bot.tree.command()
async def reload(interaction: discord.Interaction, extension: str):
    await bot.reload_extension(f"cogs.{extension}")
    await interaction.response.send_message("Reload Successfully!", ephemeral=True, delete_after=3)
    await bot.tree.sync()


@bot.tree.command()
async def unload(interaction: discord.Interaction, extension: str):
    await bot.unload_extension(f"cogs.{extension}")
    await interaction.response.send_message("Unload Successfully!", ephemeral=True, delete_after=3)
    await bot.tree.sync()


bot.run(TOKEN, log_formatter=FORMATTER, log_handler=HANDLER, root_logger=True)
