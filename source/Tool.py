import  pygame

class tool:
    registry = []

    def __init__(self, name, tool_type):
        self.name = name
        self.tool_type = tool_type
        self.max_durability = 100
        self.durability = self.max_durability = 100
        self.efficiency = 1.0
        tool.registry.append(self)

    def use(self, amount):
        if self.durability > 0:
            self.durability -= amount
            return self.durability

    def repair(self, amount):
        if self.durability < 100:
            self.durability += amount
            return self.durability

    def get_info(self):
        return {
            "name": self.name,
            "type": self.tool_type,
            "durability": self.durability,
            "efficiency": self.efficiency
        }
