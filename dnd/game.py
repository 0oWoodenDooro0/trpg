from dnd.ability import Ability
from dnd.cls import ClassEnum
from dnd.player import Player
from dnd.race import RaceEnum
from util.database import Database


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
