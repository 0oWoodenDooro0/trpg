from enum import IntEnum, unique


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
