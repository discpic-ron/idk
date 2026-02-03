import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("survival game")
clock = pygame.time.Clock()

# Constants
running = True
day_ended = False
day = 1
grid_size = 50
time_scale = 60
current_honor = 0
map_width = 800 // grid_size
map_height = 600 // grid_size
current_hour = 6
current_minute = 0
max_honor = 9999999999
total_game_seconds = 21600.0   # start at 6:00 AM
privileges = []

# Fonts
font_big = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)
ui_font = pygame.font.SysFont("Arial", 22, bold=True)

# Colors
black = (0,0,0)
white = (255,255,255)

# Sprites
sun = pygame.image.load("assets/sun.png")
moon = pygame.image.load("assets/moon.png")

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

def lose_honor(amount:
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
    screen.fill(black)
    drawClock(startDay,dt)
    screen.blit(sun, (730,0))
    sun = pygame.transform.smoothscale(sun,(64,64))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
