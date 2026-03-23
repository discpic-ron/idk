import pygame

class entity:
    registry = []
    def __init__(self,x,y,entity_type,path,animation=None):
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.max_health = 100
        self.health = self.max_health
        self.animation = animation
        entity.registry.append(self)

    def take_damage(self, amount):
        if self.health <= 0:
            return True
        self.health -= amount
        return self.health
