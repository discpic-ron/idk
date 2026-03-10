from item import Item

class Weapon(Item):
  def __init__(self,name,damage,durability,weight,animation=None,range=None,cool_down=0,stackable=False,max_stack=1):
    super().__init__(name,stackable,max_stack)
    self.name = name
    self.damage = damage
    self.max_durability = 100
    self.durability = self.max_durability
    self.range = range
    self.cool_down = cool_down
    self.last_used = 0
    self.weight = weight
    self.status_effect = "poison"
    self.status_duration = 5
    self.animation = animation
    self.broken = False

  def use(self,amount):
    if self.durability > 0:
      self.durability -= amount

  def repair(self,amount):
    if self.durability < 100:
      self.durability += amount

  def can_use(self, current_time):
    return current_time - self.last_used >= self.cooldown

  def apply_effect(self):
    pass
