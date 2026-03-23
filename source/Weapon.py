import pygame
from Item import item

class weapon(item):
    registry = []

    def __init__(self, name, image, damage, weight, animation, effect=None,ranged=False, stackable=False, max_stack=1):
        super().__init__(name, stackable, max_stack)
        self.name = name
        self.image = image
        self.max_durability = 100
        self.durability = self.max_durability
        self.damage = damage
        self.ranged = ranged
        self.weight = weight
        self.effect = effect
        self.animation = animation
        self.broken = False
        weapon.registry.append(self)

    def use(self, amount):
        if self.durability > 0:
            self.durability -= amount
            return self.durability

    def repair(self, amount):
        if self.durability < 100:
            self.durability += amount
            return self.durability

    def draw(self,screen):
        pass

    def get_info(self):
        return {
            "name": self.name,
            "damage": self.damage,
            "weight": self.weight,
            "durability": self.durability
        }
