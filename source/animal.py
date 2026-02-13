class Animal:
    def __init__(self,animal_type,speed,x,y):
        self.max_health = 100
        self.health = self.max_health
        self.speed = speed
        self.animal_type = animal_type
        self.images = []
        self.animations = []
        self.animation_state = "idle"
        self.state = "walking"

    def takeDamage(self,amount):
        self.health -= amount
        return self.health

    def changeState(self,new_state):
        self.state = new_state
        return self.state

    def changeAnimation(self,new_ani):
        self.animation_state = new_ani
        return self.animation_state
