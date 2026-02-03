class Privilege:
  def __init__(self, name, threshold):
    self.name = name
    self.threshold = threshold
    self.status = "locked"

  def update_status(self, honor_amount):
    if honor_amount >= self.threshold and self.status == "locked":
      self.status = "unlocked"
      if self.name not in privileges:
        privileges.append(self.name)
      print(f"{self.name} unlocked at {honor_amount} xp!")
