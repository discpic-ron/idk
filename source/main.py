import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("survival game")
clock = pygame.time.Clock()

# Constants
running = True
day_ended = False
day = 1
speed = 4
player_x = 0
player_y = 0
grid_size = 50
time_scale = 60
max_sprint = 100
sprint_lvl = 100
current_hour = 6
orbit_radius = 60  # Distance from player center
current_honor = 0
current_minute = 0
stamina_regen = 0.5
max_honor = 9999999999
map_width = 800 // grid_size
map_height = 600 // grid_size
total_game_seconds = 21600.0   # start at 6:00 AM
privileges = []

# Fonts
font_big = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)
ui_font = pygame.font.SysFont("Arial", 22, bold=True)

# Colors
black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
gray = (128,128,128)
red = (255,0,0)
green = (0,255,0)
brown = (150,75,0)

# Sprites
sun = pygame.image.load("assets/sun.png")
moon = pygame.image.load("assets/moon.png")
objects = [pygame.Rect(300,200,20,20)]

# Rects
sprint_bx = pygame.Rect(0,70,250,50)
drain_bx = pygame.Rect(0,70,250,50)
health_bx = pygame.Rect(0,0,250,50)
damange_bx = pygame.Rect(0,0,250,50)
player_bx = pygame.Rect(100, 200, 50, 50)
interaction_bx = pygame.Rect(200,300,50,50)
weapon_rect = pygame.Rect(0, 0, 30, 10)

# Text
interaction_txt = font_small.render("Press E to interact",white,True)

# Day system
def startDay(delta_time_seconds):
  global total_game_seconds, current_hour, current_minute

  # advance time and return formatted string
  total_game_seconds += delta_time_seconds * time_scale
  seconds_today = total_game_seconds % 86400
  current_hour = int(seconds_today // 3600) % 24
  current_minute = int(seconds_today // 60) % 60
  display_hour = current_hour % 12 or 12
  am_pm = "AM" if current_hour < 12 else "PM"
  return f"{display_hour:02d}:{current_minute:02d} {am_pm}"

def endDay():
  global day, day_ended, current_hour, current_minute
  if current_hour == 21 and current_minute == 0:  # check if shift ended and increment day
    if not day_ended:
      day += 1
      day_ended = True
      print(f"--- Shift ended. Starting Day {day}. ---")
  else:
    day_ended = False

def drawClock(start_day, dt):
  # call the endDay function and get the updated display string
  display_time_string = start_day(dt)
  current_time_surface = font_small.render(f"Time: {display_time_string}", True, white)
  day_surface = font_small.render(f"Day: {day}", True, white)
  screen.blit(current_time_surface, (2, 0))
  screen.blit(day_surface, (2, 32))
  
def grant_honor(amount):
  global current_honor,privilege_list
  current_honor += amount
  if current_honor > max_honor:
    current_honor = max_honor
  for p in privilege_list:
    p.update_status(current_honor)
  return current_honor, privileges

def lose_honor(amount):
  global current_honor,privilege_list
  current_honor -= amount
  if current_honor < 0:
    current_honor = 0
  # revoke privileges if honor drops below threshold
  for p in privilege_list:
    if current_honor < p.threshold and p.status == "unlocked":
      p.status = "locked"
      if p.name in privileges:
        privileges.remove(p.name)
      print(f"{p.name} revoked at {current_honor} Hxp!")
  return current_honor, privileges
  
while running:
  dt = clock.get_time()/1000
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
    if sprint_bx.width > 0:
      speed = 7
      sprint_bx.width -= 2
    else:
      speed = 4
  else:
    if sprint_bx.width < 250:
      sprint_bx.width += stamina_regen
      
  sprint_bx.width = max(0, min(sprint_bx.width, 250))
  health_bx.width = max(0, min(health_bx.width, 250))
  
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    player_x -= speed
    player_bx.x -= speed
  elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    player_x += speed
    player_bx.x += speed
  elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
    player_y += speed
    player_bx.y += speed
  elif keys[pygame.K_w] or keys[pygame.K_UP]:
    player_y -= speed
    player_bx.y -= speed
    
  p_center = pygame.Vector2(player_rect.center)
  m_pos = pygame.Vector2(pygame.mouse.get_pos())
  direction = m_pos - p_center # Subtract to get direction, then scale to our orbit radius
  if direction.length() > 0:  # Prevent error if mouse is on player center
    direction.scale_to_length(orbit_radius)
  weapon_rect.center = p_center + direction # The weapon's center is now p_center + the direction vector
  for i in range(len(objects)):
    if weapon_rect.colliderect(objects[i]):
      objects.pop(i)
      print("destroyed object!")
      
  if player_bx.colliderect(interaction_bx):
    screen.blit(interaction_txt,(interaction_bx.x,interaction_bx.y-20))
    if keys[pygame.K_e]:
      pass
    
  screen.fill(black)
  pygame.draw.rect(screen,red,player_bx)
  pygame.draw.rect(screen,gray,drain_bx,border_radius=20)
  pygame.draw.rect(screen,green,health_bx,border_radius=20)
  pygame.draw.rect(screen,yellow,sprint_bx,border_radius=20)
  pygame.draw.rect(screen, (255, 50, 50), weapon_rect)   # Orbiting Weapon
  drawClock(startDay,dt)
  screen.blit(sun, (730,0))
  sun = pygame.transform.smoothscale(sun,(64,64))
  for enemy_rect in objects:
    pygame.draw.rect(screen, brown, enemy_rect)
  pygame.display.flip()
  clock.tick(60)
pygame.quit()
