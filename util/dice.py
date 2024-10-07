import random


class Dice:
    @staticmethod
    def roll(times: int, sided: int) -> int:
        return sum(random.randint(1, sided) for _ in range(times))
