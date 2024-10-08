import uuid

from dnd.ability import Ability
from dnd.cls import ClassBase, ClassEnum, Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, \
    Sorcerer, Warlock, Wizard
from dnd.race import RaceBase, RaceEnum, Elf, Human, Halfling, Dwarf, Gnome, Tiefling, Dragonborn, HalfOrc


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
