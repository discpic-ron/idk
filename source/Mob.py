import pygame
import math

class mob:
    registry = []
    def __init__(self,x,y,animations,loot):
        self.x = x
        self.y = y
        self.speed = 2
        self.max_health = 100
        self.health = self.max_health
        self.animations = animations
        self.state = "idle"
        self.hostile = False
        self.loot = loot
        mob.registry.append(self)

    def take_damage(self,amount):
        self.health -= amount
        return self.health

    def draw(self):
        pass

    def move(self,target_x,target_y):
        if self.hostile == True:
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx /= dist
                dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed
        else:
            pass
