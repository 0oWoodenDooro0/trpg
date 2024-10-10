import sqlite3
import uuid
from enum import unique, IntEnum
from typing import Optional

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from context import GUILD


class Skill:
    def __init__(self, strength: int = 0, dexterity: int = 0, constitution: int = 0, intelligence: int = 0,
                 wisdom: int = 0, charisma: int = 0):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def __add__(self, other):
        if isinstance(other, Skill):
            return Skill(self.strength + other.strength, self.dexterity + other.dexterity,
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
    additional_skill = Skill()


class Elf(RaceBase):
    additional_skill = Skill(dexterity=2)


class Human(RaceBase):
    additional_skill = Skill(strength=1, dexterity=1, constitution=1, intelligence=1, wisdom=1, charisma=1)


class Halfling(RaceBase):
    additional_skill = Skill(dexterity=2)


class Dwarf(RaceBase):
    additional_skill = Skill(constitution=2)


class Gnome(RaceBase):
    additional_skill = Skill(intelligence=2)


class Tiefling(RaceBase):
    additional_skill = Skill(intelligence=1, charisma=2)


class Dragonborn(RaceBase):
    additional_skill = Skill(strength=2, charisma=1)


class HalfOrc(RaceBase):
    additional_skill = Skill(strength=2, constitution=1)


@unique
class Alignment(IntEnum):
    LAWFUL_GOOD = 0
    NEUTRAL_GOOD = 1
    CHAOTIC_GOOD = 2
    LAWFUL_NEUTRAL = 3
    NEUTRAL = 4
    CHAOTIC_NEUTRAL = 5
    LAWFUL_BAD = 6
    NEUTRAL_BAD = 7
    CHAOTIC_BAD = 8


class Character:
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

    def __init__(self, name: str, race: RaceEnum, cls: ClassEnum, skill: Skill, uid: Optional[str] = None,
                 level: int = 1, exp: int = 0, max_hit_points: Optional[int] = None, remaining_skill_points: int = 0):
        if uid is None:
            self.uid = uuid.uuid4()
        else:
            self.uid = uuid.UUID(hex=uid)
        self.name = name
        self.race_enum = race
        self.race = self.race_table[race]
        self.cls_enum = cls
        self.cls = self.class_table[cls]
        self.skill = skill
        self.level = level
        self.exp = exp
        if max_hit_points is None:
            self.max_hit_points = self.cls.first_hit
        else:
            self.max_hit_points = max_hit_points
        self.hit_points = self.max_hit_points
        self.remaining_skill_points = remaining_skill_points

    def level_up(self):
        if self.level >= 20:
            return
        if self.exp <= self.exp_table[self.level + 1]:
            return

        self.level += 1

    def show_exp(self):
        return f"{self.exp}/{self.exp_table[self.level + 1]}"

    def show_skill(self):
        return f"`STR` {self.skill.strength} `DEX` {self.skill.dexterity} `CON` {self.skill.constitution} `INT` {self.skill.intelligence} `WIS` {self.skill.wisdom} `CHA` {self.skill.charisma}"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.sqlite')
        self.cursor = self.connection.cursor()
        self.initial_tables()

    def initial_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS player(id INT, character_id TEXT)")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS character(id TEXT, name TEXT, race INT, class INT, level INT, exp INT, 
            max_hit_points INT,  strength INT, dexterity INT, constitution INT, intelligence INT, wisdom INT, 
            charisma INT)
        ''')

    def insert_character(self, uid: int, character: Character) -> None:
        skill = character.skill
        self.cursor.execute(f"INSERT INTO player(id, character_id) VALUES ({uid}, '{character.uid}')")
        self.cursor.execute(f'''
            INSERT INTO character VALUES (
            '{character.uid}', '{character.name}', {character.race_enum}, {character.cls_enum}, {character.level}, {character.exp}, 
            {character.max_hit_points}, {skill.strength}, {skill.dexterity}, {skill.constitution},
            {skill.intelligence}, {skill.wisdom}, {skill.charisma})
        ''')
        self.connection.commit()

    def find_character_by_id(self, uid: int):
        result = self.cursor.execute(f"SELECT character_id FROM player WHERE id = {uid}")
        data = result.fetchone()
        if data:
            result = self.cursor.execute(f"SELECT * FROM character WHERE id = '{data[0]}'")
            data = result.fetchone()
            return Character(uid=data[0], name=data[1], race=RaceEnum(data[2]), cls=ClassEnum(data[3]), level=data[4],
                             exp=data[5], max_hit_points=data[6],
                             skill=Skill(data[7], data[8], data[9], data[10], data[11], data[12]))


class Game:

    @classmethod
    def create_character(cls, database: Database, uid: int, name: str, race: RaceEnum, profession: ClassEnum,
                         skill: Skill) -> Character:
        character = Character(name, race, profession, skill)
        database.insert_character(uid, character)
        return character

    @classmethod
    def load_character(cls, database: Database, uid: int):
        return database.find_character_by_id(uid)


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
        if Game.load_character(self.database, interaction.user.id) is not None:
            await interaction.response.send_message("You are already create a character", ephemeral=True,
                                                    delete_after=3)
            return
        character = Game.create_character(self.database, interaction.user.id, name, RaceEnum(race.value),
                                          ClassEnum(cls.value),
                                          skill=Skill(strength, dexterity, constitution, intelligence, wisdom,
                                                      charisma))
        embed = self.embed_stats(character)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)

    @app_commands.command(name='stats')
    async def stats(self, interaction: discord.Interaction):
        character = Game.load_character(self.database, interaction.user.id)
        if character is None:
            await interaction.response.send_message("You have to create a character first", ephemeral=True,
                                                    delete_after=3)
            return
        embed = self.embed_stats(character)
        await interaction.response.send_message(embed=embed)

    @staticmethod
    def embed_stats(character: Character):
        embed = discord.Embed(title=character.name, description=character.uid)
        embed.add_field(name='Race', value=character.race.__name__, inline=True)
        embed.add_field(name='Class', value=character.cls.__name__, inline=True)
        embed.add_field(name='Level', value=character.level, inline=True)
        embed.add_field(name='Exp', value=character.show_exp(), inline=True)
        embed.add_field(name='Hit points', value=character.hit_points, inline=True)
        embed.add_field(name='Ability', value=character.show_skill(), inline=False)
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot), guild=GUILD)
    await bot.tree.sync(guild=GUILD)
