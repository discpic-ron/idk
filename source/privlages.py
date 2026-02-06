class Privilege:
  privilege_list = []
  
  def __init__(self, name, threshold):
    self.name = name
    self.threshold = threshold
    self.status = "locked"
    
  def update_status(self,current_honor):
    if current_honor >= self.threshold and self.status == "locked":
      self.status = "unlocked"
      if self.name not in privileges:
        privileges.append(self.name)
      print(f"{self.name} unlocked at {current_honor} xp!")
      
  def grant_honor(self,amount,current_honor):
    current_honor += amount
    if current_honor > self.threshold:
      current_honor = self.threshold
    for p in Privilege.privilege_list:
      p.update_status(current_honor)
    return current_honor, privileges
  
  def lose_honor(self, amount, current_honor):
    current_honor -= amount
    if current_honor < 0:
      current_honor = 0
    # revoke privileges if honor drops below threshold
    for p in Privilege.privilege_list:
      if current_honor < p.threshold and p.status == "unlocked":
        p.status = "locked"
        if p.name in privileges:
          privileges.remove(p.name)
        print(f"{p.name} revoked at {current_honor} Hxp!")
    return current_honor, privileges
