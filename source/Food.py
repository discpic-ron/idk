import pygame
from Item import item

class food(item):
    registry = []
    def __init__(self, name, image,food_value, effect=None, stackable=True, max_stack=99):
        super().__init__(name, stackable, max_stack)
        self.name = name
        self.image = image
        self.food_value = food_value
        self.effect = effect

    def apply(self, player):
        if self.effect == "hunger":
            player.hunger += self.food_value

        elif self.effect == "thirst":
            player.thirst += self.food_value

    def draw(self):
        pass

    def get_info(self):
        return {
            "name": self.name,
            "effect": self.effect,
            "value": self.food_value
        }
