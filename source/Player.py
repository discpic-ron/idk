import pygame

class player:
    def __init__(self,x,y,inventory,animations,speed=4):
        self.x  = x
        self.y = y
        self.animations = animations
        self.max_health = 100
        self.health = self.max_health
        self.thirst = 100
        self.hunger = 100
        self.sanity = 100
        self.honor = 0
        self.speed = speed
        self.inventory = inventory
        self.team = []
        self.state = "idle"

    def take_damage(self, amount):
        if self.health <= 0:
            return True
        self.health -= amount
        return self.health

    def heal(self,amount):
        self.health += amount
        return self.health

    def increase_sanity(self,amount):
        self.sanity += amount
        return self.sanity

    def decrease_sanity(self,amount):
        self.sanity -= amount
        return self.sanity

    def increase_honor(self,amount):
        self.honor += amount
        return self.honor

    def decrease_honor(self,amount):
        self.honor -= amount
        return self.honor

    def update(self):
        pass

    def draw(self):
        pass
