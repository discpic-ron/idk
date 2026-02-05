class Item:
    def __init__(self, name, description, damage, classification):
        self.name = name
        self.description = description
        self.damage = damage
        self.classification = classification

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description
