import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from context import GUILD, LOGGER
from dnd.cls import ClassEnum
from dnd.game import Game
from dnd.player import Ability, Player
from dnd.race import RaceEnum
from util.database import Database


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()

    @app_commands.command(name='create')
    @app_commands.describe(name="name of the character", race="race of the character", cls="class of the character")
    @app_commands.choices(race=[
        Choice(name='elf', value=RaceEnum.ELF),
        Choice(name='human', value=RaceEnum.HUMAN),
        Choice(name='halfling', value=RaceEnum.HALFLING),
        Choice(name='dwarf', value=RaceEnum.DWARF),
        Choice(name='gnome', value=RaceEnum.GNOME),
        Choice(name='tiefling', value=RaceEnum.TIEFLING),
        Choice(name='dragonborn', value=RaceEnum.DRAGONBORN),
        Choice(name='half orc', value=RaceEnum.HALF_ORC)
    ])
    @app_commands.choices(cls=[
        Choice(name='barbarian', value=ClassEnum.BARBARIAN),
        Choice(name='bard', value=ClassEnum.BARD),
        Choice(name='cleric', value=ClassEnum.CLERIC),
        Choice(name='druid', value=ClassEnum.DRUID),
        Choice(name='fighter', value=ClassEnum.FIGHTER),
        Choice(name='monk', value=ClassEnum.MONK),
        Choice(name='paladin', value=ClassEnum.PALADIN),
        Choice(name='ranger', value=ClassEnum.RANGER),
        Choice(name='rogue', value=ClassEnum.ROGUE),
        Choice(name='sorcerer', value=ClassEnum.SORCERER),
        Choice(name='warlock', value=ClassEnum.WARLOCK),
        Choice(name='wizard', value=ClassEnum.WIZARD)
    ])
    async def create(self, interaction: discord.Interaction, name: str, race: Choice[int],
                     cls: Choice[int], strength: int, dexterity: int, constitution: int, intelligence: int,
                     wisdom: int, charisma: int):
        if Game.load_player(self.database, interaction.user.id) is not None:
            await interaction.response.send_message("You are already create a character", ephemeral=True,
                                                    delete_after=3)
            return
        player = Game.create_player(self.database, interaction.user.id, name, RaceEnum(race.value),
                                    ClassEnum(cls.value),
                                    ability=Ability(strength, dexterity, constitution, intelligence, wisdom, charisma))
        embed = self.stats(player)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)

    @staticmethod
    def stats(player: Player):
        embed = discord.Embed(title=player.name, description=player.uid)
        embed.add_field(name='Race', value=player.race.__class__.__name__, inline=True)
        embed.add_field(name='Class', value=player.cls.__class__.__name__, inline=True)
        embed.add_field(name='Level', value=player.level, inline=True)
        embed.add_field(name='Exp', value=player.show_exp(), inline=True)
        embed.add_field(name='Hit points', value=player.hit_points, inline=True)
        embed.add_field(name='Ability', value=player.show_ability(), inline=False)
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot), guild=GUILD)
    await bot.tree.sync(guild=GUILD)
