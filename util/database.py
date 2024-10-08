import sqlite3

from dnd.ability import Ability
from dnd.cls import ClassEnum
from dnd.player import Player
from dnd.race import RaceEnum


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
