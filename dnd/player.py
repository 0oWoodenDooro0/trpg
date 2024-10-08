import uuid

from dnd.ability import Ability
from dnd.cls import ClassBase
from dnd.race import RaceBase


class Player:
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

    def __init__(self, name: str, race: RaceBase, cls: ClassBase, ability: Ability):
        self.uid = uuid.uuid4()
        self.name = name
        self.race = race
        self.cls = cls
        self.ability = ability
        self.level = 1
        self.hit_points = self.cls.first_hit
        self.exp = 0

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
