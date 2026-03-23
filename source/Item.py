class item:

    def __init__(self, name, stackable=True, max_stack=99,weight=1.0):
        self.name = name
        self.stackable = stackable
        self.max_stack = max_stack
        self.weight = weight
        self.current_stack = 0

    def add_stack(self):
        if self.current_stack <= self.max_stack:
            self.current_stack += 1
            return self.current_stack

    def remove_stack(self):
        if self.current_stack <= self.max_stack:
            self.current_stack -= 1
            return self.current_stack

    def get_info(self):
        return {
            "name": self.name,
            "count": self.current_stack
        }
