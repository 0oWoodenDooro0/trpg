from dnd.player import Player, Ability
from dnd.race import RaceEnum, Elf, Human, Halfing, Dwarf, Gnome, Tiefling, Dragonborn, HalfOrc


class Game:
    race_transfer = {
        RaceEnum.ELF: Elf,
        RaceEnum.HUMAN: Human,
        RaceEnum.HALFLING: Halfing,
        RaceEnum.DWARF: Dwarf,
        RaceEnum.GNOME: Gnome,
        RaceEnum.TIEFLING: Tiefling,
        RaceEnum.DRAGONBORN: Dragonborn,
        RaceEnum.HALF_ORC: HalfOrc,
    }

    @classmethod
    def create_player(cls, name: str, race: RaceEnum, ability: Ability):
        player = Player(name, cls.race_transfer[race](), ability)
