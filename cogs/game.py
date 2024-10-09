import sqlite3
import uuid
from enum import unique, IntEnum

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from context import GUILD


class Ability:
    def __init__(self, strength: int = 0, dexterity: int = 0, constitution: int = 0, intelligence: int = 0,
                 wisdom: int = 0, charisma: int = 0):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def __add__(self, other):
        if isinstance(other, Ability):
            return Ability(self.strength + other.strength, self.dexterity + other.dexterity,
                           self.constitution + other.constitution, self.intelligence + other.intelligence,
                           self.wisdom + other.wisdom, self.charisma + other.charisma)
        raise TypeError("Ability only can add with Ability.")


@unique
class ClassEnum(IntEnum):
    BARBARIAN = 0
    BARD = 1
    CLERIC = 2
    DRUID = 3
    FIGHTER = 4
    MONK = 5
    PALADIN = 6
    RANGER = 7
    ROGUE = 8
    SORCERER = 9
    WARLOCK = 10
    WIZARD = 11


class ClassBase:
    hit_dice = ""
    first_hit = 0


class Barbarian(ClassBase):
    hit_dice = "1d12"
    first_hit = 12


class Bard(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Cleric(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Druid(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Fighter(ClassBase):
    hit_dice = "1d10"
    first_hit = 10


class Monk(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Paladin(ClassBase):
    hit_dice = "1d10"
    first_hit = 10


class Ranger(ClassBase):
    hit_dice = "1d10"
    first_hit = 10


class Rogue(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Sorcerer(ClassBase):
    hit_dice = "1d6"
    first_hit = 6


class Warlock(ClassBase):
    hit_dice = "1d8"
    first_hit = 8


class Wizard(ClassBase):
    hit_dice = "1d6"
    first_hit = 6


@unique
class RaceEnum(IntEnum):
    ELF = 0
    HUMAN = 1
    HALFLING = 2
    DWARF = 3
    GNOME = 4
    TIEFLING = 5
    DRAGONBORN = 6
    HALF_ORC = 7


class RaceBase:
    additional_ability = Ability()


class Elf(RaceBase):
    additional_ability = Ability(dexterity=2)


class Human(RaceBase):
    additional_ability = Ability(strength=1, dexterity=1, constitution=1, intelligence=1, wisdom=1, charisma=1)


class Halfling(RaceBase):
    additional_ability = Ability(dexterity=2)


class Dwarf(RaceBase):
    additional_ability = Ability(constitution=2)


class Gnome(RaceBase):
    additional_ability = Ability(intelligence=2)


class Tiefling(RaceBase):
    additional_ability = Ability(intelligence=1, charisma=2)


class Dragonborn(RaceBase):
    additional_ability = Ability(strength=2, charisma=1)


class HalfOrc(RaceBase):
    additional_ability = Ability(strength=2, constitution=1)


class Player:
    race_table = {
        RaceEnum.ELF: Elf,
        RaceEnum.HUMAN: Human,
        RaceEnum.HALFLING: Halfling,
        RaceEnum.DWARF: Dwarf,
        RaceEnum.GNOME: Gnome,
        RaceEnum.TIEFLING: Tiefling,
        RaceEnum.DRAGONBORN: Dragonborn,
        RaceEnum.HALF_ORC: HalfOrc,
    }
    class_table = {
        ClassEnum.BARBARIAN: Barbarian,
        ClassEnum.BARD: Bard,
        ClassEnum.CLERIC: Cleric,
        ClassEnum.DRUID: Druid,
        ClassEnum.FIGHTER: Fighter,
        ClassEnum.MONK: Monk,
        ClassEnum.PALADIN: Paladin,
        ClassEnum.RANGER: Ranger,
        ClassEnum.ROGUE: Rogue,
        ClassEnum.SORCERER: Sorcerer,
        ClassEnum.WARLOCK: Warlock,
        ClassEnum.WIZARD: Wizard
    }
    exp_table = {
        1: 0,
        2: 300,
        3: 900,
        4: 2700,
        5: 6500,
        6: 14000,
        7: 23000,
        8: 34000,
        9: 48000,
        10: 64000,
        11: 85000,
        12: 100000,
        13: 120000,
        14: 140000,
        15: 165000,
        16: 195000,
        17: 225000,
        18: 265000,
        19: 305000,
        20: 355000
    }

    def __init__(self, name: str, race: RaceEnum, cls: ClassEnum, ability: Ability, uid: int = None,
                 level: int = 1, exp: int = 0):
        if uid is None:
            self.uid = uuid.uuid4().int
        else:
            self.uid = uid
        self.name = name
        self.race = self.race_table[race]
        self.cls = self.class_table[cls]
        self.ability = ability
        self.level = level
        self.hit_points = self.cls.first_hit
        self.exp = exp

    def level_up(self):
        if self.level >= 20:
            return
        if self.exp <= self.exp_table[self.level + 1]:
            return

        self.level += 1

    def show_exp(self):
        return f"{self.exp}/{self.exp_table[self.level]}"

    def show_ability(self):
        return f"`STR` {self.ability.strength} `DEX` {self.ability.dexterity} `CON` {self.ability.constitution} `INT` {self.ability.intelligence} `WIS` {self.ability.wisdom} `CHA` {self.ability.charisma}"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.sqlite')
        self.cursor = self.connection.cursor()
        self.initial_tables()

    def initial_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player(id INT, character_id INT)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS character(id INT, name TEXT, race INT, class INT, level INT, exp INT, "
            "strength INT, dexterity INT, constitution INT, intelligence INT, wisdom INT, charisma INT)")

    def insert_player(self, uid: int, character_id: int, name: str, race: int, cls: int, level: int, exp: int,
                      strength: int, dexterity: int, constitution: int, intelligence: int, wisdom: int,
                      charisma: int) -> None:
        self.cursor.execute(f"INSERT INTO player(id, character_id) VALUES ({uid}, {character_id})")
        self.cursor.execute(
            f"INSERT INTO character(id, name, race, class, level, exp, "
            f"strength, dexterity, constitution, intelligence, wisdom, charisma) VALUES ("
            f"{character_id}, '{name}', {race}, {cls}, {level}, {exp}, "
            f"{strength}, {dexterity}, {constitution}, {intelligence}, {wisdom}, {charisma})")
        self.connection.commit()

    def find_player_by_id(self, uid: int):
        result = self.cursor.execute(f"SELECT character_id FROM player WHERE id = {uid}")
        data = result.fetchone()
        if data:
            result = self.cursor.execute(f"SELECT * FROM character WHERE id = {data[0]}")
            data = result.fetchone()
            return Player(uid=data[0], name=data[1], race=RaceEnum(data[2]), cls=ClassEnum(data[3]), level=data[4],
                          exp=data[5], ability=Ability(data[6], data[7], data[8], data[9], data[10], data[11]))


class Game:

    @classmethod
    def create_player(cls, database: Database, uid: int, name: str, race: RaceEnum, profession: ClassEnum,
                      ability: Ability) -> Player:
        player = Player(name, race, profession, ability)
        database.insert_player(uid, player.uid, player.name, race, profession, player.level, player.exp,
                               player.ability.strength, player.ability.dexterity, player.ability.constitution,
                               player.ability.intelligence, player.ability.wisdom, player.ability.charisma)
        return player

    @classmethod
    def load_player(cls, database: Database, uid: int):
        return database.find_player_by_id(uid)


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
