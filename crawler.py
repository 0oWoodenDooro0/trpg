import asyncio
import re
import sqlite3

import requests
from bs4 import BeautifulSoup

from cogs.game import Skill, Monster, AlignmentEnum


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.sqlite')
        self.cursor = self.connection.cursor()
        self.initial_tables()

    def initial_tables(self):
        self.cursor.execute('''DROP TABLE IF EXISTS monster''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS monster(name TEXT, alignment INT, armor_class INT, hit_points_dice_times int, 
            hit_points_dice_sided int, hit_points_fixed INT, skill_strength INT, skill_dexterity INT,
            skill_constitution INT, skill_intelligence INT, skill_wisdom INT, skill_charisma INT, challenge TEXT)
        ''')

    def insert_monster(self, monster):
        self.cursor.execute(f'''
            INSERT INTO monster VALUES (
            ?, {monster.alignment}, {monster.armor_class}, {monster.hit_points_dice_times}, 
            {monster.hit_points_dice_sided}, {monster.hit_points_fixed}, {monster.skill.strength},
            {monster.skill.dexterity}, {monster.skill.constitution}, {monster.skill.intelligence}, 
            {monster.skill.wisdom}, {monster.skill.charisma}, '{monster.challenge}')
        ''', (monster.name,))
        self.connection.commit()


class Crawler:
    alignment_table = {
        "Lawful Good": AlignmentEnum.LAWFUL_GOOD,
        "Neutral Good": AlignmentEnum.NEUTRAL_GOOD,
        "Chaotic Good": AlignmentEnum.CHAOTIC_GOOD,
        "Lawful Neutral": AlignmentEnum.LAWFUL_NEUTRAL,
        "Neutral": AlignmentEnum.NEUTRAL,
        "Chaotic Neutral": AlignmentEnum.CHAOTIC_NEUTRAL,
        "Lawful Evil": AlignmentEnum.LAWFUL_EVIL,
        "Neutral Evil": AlignmentEnum.NEUTRAL_EVIL,
        "Chaotic Evil": AlignmentEnum.CHAOTIC_EVIL,
        "Unaligned": AlignmentEnum.UNALIGNED,
        "Any Alignment": AlignmentEnum.ANY_ALIGNMENT,
        "Any Chaotic Alignment": AlignmentEnum.ANY_CHAOTIC_ALIGNMENT,
        "Any evil alignment": AlignmentEnum.ANY_EVIL_ALIGNMENT,
        "Any Non-Lawful Alignment": AlignmentEnum.ANY_NON_LAWFUL_ALIGNMENT,
        "Any Non-Chaotic Alignment": AlignmentEnum.ANY_NON_CHAOTIC_ALIGNMENT,
        "Any Non-Good Alignment": AlignmentEnum.ANY_NON_GOOD_ALIGNMENT,
    }

    @staticmethod
    async def get_monsters(database: Database):
        base_url = "https://dnd-wiki.org"
        urls = ["https://dnd-wiki.org/wiki/Category:SRD5_Monsters",
                "https://dnd-wiki.org/w/index.php?title=Category:SRD5_Monsters&pagefrom=Medusa+AAA+Common+5e%0AMedusa#mw-pages"]
        wiki_links = []
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            categories = soup.find_all("div", {"class": "mw-category-group"})
            for category in categories:
                relative_urls = (a["href"] for a in category.find_all("a"))
                wiki_links.extend((base_url + relative_url for relative_url in relative_urls))

        for link in wiki_links:
            monster = await Crawler.get_monster(link)
            if monster is None:
                print(link)
            else:
                database.insert_monster(monster)
        print("end!")

    @staticmethod
    async def get_monster(url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        detail = soup.find("table", {"class": "left monstats"})
        if detail is None:
            return
        name = detail.find("b").text
        alignment = detail.find("i").find_all("a")[-1].text
        alignment_enum = Crawler.alignment_table.get(alignment, None)
        armor_class = None
        hit_points_dice_times = None
        hit_points_dice_sided = None
        hit_points_fixed = None
        skill = None
        challenge = None
        for column in detail.find_all("tr"):
            match = re.match(r'\s*Armor Class:\s*(\d+)', column.text)
            if match is not None:
                armor_class = match.group(1)
                continue
            match = re.match(r'\s*Hit Points:\s+\d+\s+\((\d+)d(\d+)([\+\-]\d+)?\)', column.text)
            if match is not None:
                hit_points_dice_times = match.group(1)
                hit_points_dice_sided = match.group(2)
                if match.group(3) is not None:
                    hit_points_fixed = match.group(3)
                else:
                    hit_points_fixed = "0"
                continue
            skill_table = column.find("table")
            if skill_table is not None:
                table = skill_table.find_all("tr")[-1].find_all("td")
                skill_compile = re.compile(r'\s*(\d+)\s+\([\+\-]\d+\)')
                if skill_compile.match(table[0].text) and skill_compile.match(table[1].text) and skill_compile.match(
                        table[2].text) and skill_compile.match(table[3].text) and skill_compile.match(
                    table[4].text) and skill_compile.match(table[5].text):
                    skill = Skill(skill_compile.match(table[0].text).group(1),
                                  skill_compile.match(table[1].text).group(1),
                                  skill_compile.match(table[2].text).group(1),
                                  skill_compile.match(table[3].text).group(1),
                                  skill_compile.match(table[4].text).group(1),
                                  skill_compile.match(table[5].text).group(1))
            match = re.match(r'\s*Challenge:\s*([\d\/]+)\s*\([\d,]+\s*xp\)', column.text)
            if match is not None:
                challenge = match.group(1)

        if name and alignment_enum is not None and armor_class is not None and hit_points_dice_times is not None and hit_points_dice_sided is not None and hit_points_fixed is not None and skill and challenge is not None:
            return Monster(name=name, alignment=alignment_enum, armor_class=int(armor_class),
                           hit_points_dice_times=int(hit_points_dice_times),
                           hit_points_dice_sided=int(hit_points_dice_sided),
                           hit_points_fixed=int(hit_points_fixed), skill=skill, challenge=challenge)
        print(name)
        print(alignment)
        print(alignment_enum)
        print(armor_class)
        print(hit_points_dice_times)
        print(hit_points_dice_sided)
        print(hit_points_fixed)
        print(skill)
        print(challenge)


if __name__ == '__main__':
    asyncio.run(Crawler.get_monsters(Database()))
