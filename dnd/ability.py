class Ability:
    def __init__(self, strength: int = 0, dexterity: int = 0, constitution: int = 0, intelligence: int = 0,
                 wisdom: int = 0, charisma: int = 0):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def __add__(self, other):
        if isinstance(other, Ability):
            return Ability(self.strength + other.strength, self.dexterity + other.dexterity,
                           self.constitution + other.constitution, self.intelligence + other.intelligence,
                           self.wisdom + other.wisdom, self.charisma + other.charisma)
        raise TypeError("Ability only can add with Ability.")
