class Weapon:
    def __init__(self):
        self.ammo = 0

    def shoot(self):
        self.ammo -= 1

    def reload(self, amount):
        self.ammo += amount
