class Item:
    def __init__(self, name, description, damage, item_type):
        self.name = name
        self.description = description
        self.damage = damage
        self.item_type = item_type
        self.is_weapon = False
    
    def getName(self):
        return self.name

    def getDescription(self):
        return self.description
