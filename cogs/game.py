import random
import sqlite3
import uuid
from enum import unique, IntEnum, auto
from typing import Optional

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from cogs.dice import Dice
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

    def show(self):
        return f"`STR` {self.strength} `DEX` {self.dexterity} `CON` {self.constitution} `INT` {self.intelligence} `WIS` {self.wisdom} `CHA` {self.charisma}"


@unique
class ClassEnum(IntEnum):
    BARBARIAN = auto()
    BARD = auto()
    CLERIC = auto()
    DRUID = auto()
    FIGHTER = auto()
    MONK = auto()
    PALADIN = auto()
    RANGER = auto()
    ROGUE = auto()
    SORCERER = auto()
    WARLOCK = auto()
    WIZARD = auto()


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
    ELF = auto()
    HUMAN = auto()
    HALFLING = auto()
    DWARF = auto()
    GNOME = auto()
    TIEFLING = auto()
    DRAGONBORN = auto()
    HALF_ORC = auto()


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


@unique
class AlignmentEnum(IntEnum):
    LAWFUL_GOOD = auto()
    NEUTRAL_GOOD = auto()
    CHAOTIC_GOOD = auto()
    LAWFUL_NEUTRAL = auto()
    NEUTRAL = auto()
    CHAOTIC_NEUTRAL = auto()
    LAWFUL_EVIL = auto()
    NEUTRAL_EVIL = auto()
    CHAOTIC_EVIL = auto()
    UNALIGNED = auto()
    ANY_ALIGNMENT = auto()
    ANY_CHAOTIC_ALIGNMENT = auto()
    ANY_EVIL_ALIGNMENT = auto()
    ANY_NON_LAWFUL_ALIGNMENT = auto()
    ANY_NON_CHAOTIC_ALIGNMENT = auto()
    ANY_NON_GOOD_ALIGNMENT = auto()


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

    def __init__(self, name: str, race: RaceEnum, cls: ClassEnum, ability: Ability, uid: Optional[str] = None,
                 level: int = 1, exp: int = 0, max_hit_points: Optional[int] = None, remaining_ability_points: int = 0):
        if uid is None:
            self.uid = uuid.uuid4()
        else:
            self.uid = uuid.UUID(hex=uid)
        self.name = name
        self.race_enum = race
        self.race = self.race_table[race]
        self.cls_enum = cls
        self.cls = self.class_table[cls]
        self.ability = ability
        self.level = level
        self.exp = exp
        if max_hit_points is None:
            self.max_hit_points = self.cls.first_hit
        else:
            self.max_hit_points = max_hit_points
        self.hit_points = self.max_hit_points
        self.remaining_ability_points = remaining_ability_points

    def level_up(self):
        if self.level >= 20:
            return
        if self.exp <= self.exp_table[self.level + 1]:
            return

        self.level += 1

    def show_exp(self):
        return f"{self.exp}/{self.exp_table[self.level + 1]}"


class Monster:
    challenge_table = {
        "0": 10,
        "1/8": 25,
        "1/4": 50,
        "1/2": 100,
        "1": 200,
        "2": 450,
        "3": 700,
        "4": 1100,
        "5": 1800,
        "6": 2300,
        "7": 2900,
        "8": 3900,
        "9": 5000,
        "10": 5900,
        "11": 7200,
        "12": 8400,
        "13": 1000,
        "14": 11500,
        "15": 13000,
        "16": 15000,
        "17": 18000,
        "18": 20000,
        "19": 22000,
        "20": 25000,
        "21": 33000,
        "22": 41000,
        "23": 50000,
        "24": 62000,
        "25": 75000,
        "26": 90000,
        "27": 105000,
        "28": 120000,
        "29": 135000,
        "30": 155000,
    }

    def __init__(self, name: str, alignment: AlignmentEnum, armor_class: int, hit_points_dice_times: int,
                 hit_points_dice_sided: int, hit_points_fixed: int, ability: Ability, challenge: str):
        self.name = name
        self.alignment = alignment
        self.armor_class = armor_class
        self.hit_points_dice_times = hit_points_dice_times
        self.hit_points_dice_sided = hit_points_dice_sided
        self.hit_points_fixed = hit_points_fixed
        self.max_hit_points = self.roll_hit_points(hit_points_dice_times, hit_points_dice_sided, hit_points_fixed)
        self.hit_points = self.max_hit_points
        self.ability = ability
        self.challenge = challenge
        self.exp = self.challenge_table[challenge]

    @staticmethod
    def roll_hit_points(times: int, sided: int, fixed: int):
        return Dice.roll(times, sided) + fixed


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
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS monster(name TEXT, alignment INT, armor_class INT, hit_points_dice_times int, 
            hit_points_dice_sided int, hit_points_fixed INT, ability_strength INT, ability_dexterity INT,
            ability_constitution INT, ability_intelligence INT, ability_wisdom INT, ability_charisma INT, challenge TEXT)
        ''')

    def insert_character(self, uid: int, character: Character) -> None:
        ability = character.ability
        self.cursor.execute(f"INSERT INTO player(id, character_id) VALUES ({uid}, '{character.uid}')")
        self.cursor.execute(f'''
            INSERT INTO character VALUES (
            '{character.uid}', '{character.name}', {character.race_enum}, {character.cls_enum}, {character.level}, {character.exp}, 
            {character.max_hit_points}, {ability.strength}, {ability.dexterity}, {ability.constitution},
            {ability.intelligence}, {ability.wisdom}, {ability.charisma})
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
                             ability=Ability(data[7], data[8], data[9], data[10], data[11], data[12]))

    def find_monsters_by_challenge(self, challenge: str):
        result = self.cursor.execute(f"SELECT * FROM monster WHERE challenge = '{challenge}'")
        data_list = result.fetchall()
        if data_list:
            return [Monster(name=data[0], alignment=AlignmentEnum(data[1]), armor_class=data[2],
                            hit_points_dice_times=data[3], hit_points_dice_sided=data[4], hit_points_fixed=data[5],
                            ability=Ability(data[6], data[7], data[8], data[9], data[10], data[11]), challenge=data[12])
                    for
                    data in data_list]


class Game:

    @classmethod
    def create_character(cls, database: Database, uid: int, name: str, race: RaceEnum, profession: ClassEnum,
                         ability: Ability) -> Character:
        character = Character(name, race, profession, ability)
        database.insert_character(uid, character)
        return character

    @classmethod
    def load_character(cls, database: Database, uid: int):
        return database.find_character_by_id(uid)

    @classmethod
    def load_monster_by_challenge(cls, database: Database, challenge: str):
        monsters = database.find_monsters_by_challenge(challenge)
        if monsters:
            return random.choice(monsters)


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
                                          ability=Ability(strength, dexterity, constitution, intelligence, wisdom,
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

    @app_commands.command(name='monster')
    async def monster(self, interaction: discord.Interaction, challenge: str):
        monster = Game.load_monster_by_challenge(self.database, challenge)
        if monster is None:
            await interaction.response.send_message("No monster found", ephemeral=True, delete_after=3)
            return
        embed = self.embed_monster(monster)
        await interaction.response.send_message(embed=embed)

    @staticmethod
    def embed_stats(character: Character):
        embed = discord.Embed(title=character.name, description=character.uid)
        embed.add_field(name='Race', value=character.race.__name__, inline=True)
        embed.add_field(name='Class', value=character.cls.__name__, inline=True)
        embed.add_field(name='Level', value=character.level, inline=True)
        embed.add_field(name='Exp', value=character.show_exp(), inline=True)
        embed.add_field(name='Hit points', value=character.hit_points, inline=True)
        embed.add_field(name='Ability', value=character.ability.show(), inline=False)
        return embed

    @staticmethod
    def embed_monster(monster: Monster):
        embed = discord.Embed(title=monster.name, description=monster.alignment.name)
        embed.add_field(name='Armor Class', value=monster.armor_class, inline=True)
        embed.add_field(name='Hit Points', value=monster.max_hit_points, inline=True)
        embed.add_field(name='Challenge', value=monster.challenge, inline=True)
        embed.add_field(name='Ability', value=monster.ability.show(), inline=False)
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot), guild=GUILD)
    await bot.tree.sync(guild=GUILD)
