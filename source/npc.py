import pygame
import random

class npc:
  registry = []

  def __init__(self,frames):
    self.gender, self.name = self.generateName()
    self.max_health = 100
    self.health = self.max_health
    self.morale = 100
    self.speed = random.uniform(0.5, 1.5)
    self.frames = frames
    self.frame_index = 0
    self.frame_timer = 0
    self.frame_speed = 8
    self.is_moving = False
    npc.registry.append(self)

  def generateName(self):
    male_first = ["John", "Michael", "David", "Daniel", "James", "Robert", "Matthew", "Anthony"]
    female_first = ["Sarah", "Emily", "Jessica", "Laura", "Sophia", "Olivia", "Emma", "Isabella"]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
        "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez",
        "Lopez", "Gonzalez", "Wilson", "Anderson"
    ]
    if random.choice([True, False]):
        first = random.choice(male_first)
        gender = "Male"
    else:
        first = random.choice(female_first)
        gender = "Female"
  
    last = random.choice(last_names)
    return gender, f"{first} {last}"

def boostMorale(self):
  if self.morale < 50:
      self.morale += 10
  return self.morale

def showStats(self):
  return {
      "name": self.name,
      "gender": self.gender,
      "morale": self.morale,
      "efficiency": self.base_efficiency,
      "payroll": self.payroll
  }
