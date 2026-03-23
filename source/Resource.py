import pygame
from Item import item

class resource(item):
    registry = []

    def __init__(self,name,type,image):
        super().__init__(name)
        self.name = name
        self.type = type
        resource.registry.append(self)

    def draw(self,screen):
        pass

    def get_info(self):
        return {
            "name":self.name,
            "type": self.type
        }
