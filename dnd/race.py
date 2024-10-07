from enum import unique, IntEnum

from game.player import Ability


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


class Halfing(RaceBase):
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
