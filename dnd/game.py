from dnd.ability import Ability
from dnd.player import Player
from dnd.cls import ClassEnum, Barbarian, Cleric, Druid, Fighter, Monk, Paladin, Sorcerer, Warlock, Wizard, Bard, \
    Ranger, Rogue
from dnd.race import RaceEnum, Elf, Human, Halfling, Dwarf, Gnome, Tiefling, Dragonborn, HalfOrc


class Game:
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

    @classmethod
    def create_player(cls, name: str, race: RaceEnum, profession: ClassEnum, ability: Ability):
        return Player(name, cls.race_table[race](), cls.class_table[profession](), ability)
