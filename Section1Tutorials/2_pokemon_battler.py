import random
import time

# Move types
# Constants typically all caps
FIRE = "FIRE"
WATER = "WATER"
GRASS = "GRASS"


class Pokemon:
    def __init__(self, name, initHp, type):
        self.name = name
        self.hp = initHp
        self.strength = 20
        self.type = type

    def attack(self, otherPokemon):
        # deal damage based on super effective

        # note we need to use self to call methods within own class

        bonusMultipler = self.getBonusMultiplier(otherPokemon)
        randomnessFactor = random.uniform(0.7, 1.3)  # generate random number between 0.7 and 1.3
        otherPokemon.hp -= self.strength - bonusMultipler - randomnessFactor
        otherPokemon.hp = max(0, otherPokemon.hp)  # prevent hp from going negative

    def isFainted(self):
        return self.hp <= 0

    def getBonusMultiplier(self, otherPokemon):
        SUPER_EFFECTIVE = 2
        NOT_VERY_EFFECTIVE = 0.5

        bonusMultipler = 1
        if self.type == FIRE and self.type == WATER:
            return NOT_VERY_EFFECTIVE
        elif self.type == WATER and self.type == FIRE:
            return SUPER_EFFECTIVE
        elif self.type == GRASS and self.type == FIRE:
            return NOT_VERY_EFFECTIVE
        elif self.type == FIRE and self.type == GRASS:
            return SUPER_EFFECTIVE
        elif self.type == WATER and self.type == GRASS:
            return NOT_VERY_EFFECTIVE
        elif self.type == GRASS and self.type == WATER:
            return SUPER_EFFECTIVE
        else:
            # note this is redundant, but sometimes better to clarify
            return 1


# create pokemon
bulbasaur = Pokemon("Bulbasaur", 100, GRASS)
charmander = Pokemon("Charmander", 80, FIRE)
charmander.strength = 25
squirtle = Pokemon("Squirtle", 110, WATER)
squirtle.strength = 15

# A "tuple", which uses () instead of [], behaves almost like a list
# Tuples are "immutable", which means they can't be modified after they are created
# So you can't append to a tuple or change the elements in a tuple, which can be useful
# We could have used a list instead, i.e. [[charmander, squirtle], [bulbasaur, squirtle], [bulbasaur, charmander]]
rounds = [(charmander, squirtle), (bulbasaur, squirtle), (bulbasaur, charmander)]

# rounds is a list of tuples
for round in rounds:
    contestant1 = round[0]  # you access elements in a tuple the same as in a list
    contestant2 = round[1]
    print("--------------------------------------------------")
    print(contestant1.name + " VS " + contestant2.name)
    print("--------------------------------------------------")

    while (True):
        contestant1.attack(contestant2)
        print(contestant1.name + " attacked " + contestant2.name)
        print(contestant1.name + ":" + str(contestant1.hp) + " HP")
        print(contestant2.name + ":" + str(contestant2.hp) + " HP")
        print("--------------------------------------------------")

        if contestant2.isFainted():
            print(contestant2.name + " fainted!")
            print(contestant1.name + " wins!")
            break

        contestant2.attack(contestant1)

        print(contestant2.name + " attacked " + contestant1.name)
        print(contestant1.name + ":" + str(contestant1.hp) + " HP")
        print(contestant2.name + ":" + str(contestant2.hp) + " HP")
        print("--------------------------------------------------")

        if contestant1.isFainted():
            print(contestant1.name + "fainted!")
            print(contestant2.name + 'wings!')
            break

        time.sleep(0.5)  # delays for 0.5 seconds
