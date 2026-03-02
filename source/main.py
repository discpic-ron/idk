import pygame
import math
import random

pygame.init()
SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Infinite World - Moving Animals")
clock = pygame.time.Clock()

def load_asset(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))
    except:
        surf = pygame.Surface((size, size))
        surf.fill((255, 0, 255))
        print(f"❌ ERROR: Could not find {filename} at {path}")
        return surf

TILE_SIZE = 32
grass_img = load_asset("grass.png", TILE_SIZE)
tree_img  = load_asset("tree.png", TILE_SIZE)
rock_img  = load_asset("rock_0.png", TILE_SIZE)
running = True
speed = 4
stamina_regen = 0.5
CHUNK_SIZE = 10 
WIDTH, HEIGHT = 40, 30
SCALE = 0.1
WATER_LEVEL = -0.15
SAND_LEVEL = -0.05
GRASS_LEVEL = 0.35
world_w, world_h = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
offset_x, offset_y = 0, 0
gradients = {}
player_bx = pygame.Rect(world_w//2, world_h//2, 40, 40)
sprint_width = 250
object_data = {} 
animals = []

# Colors
black, white, yellow, gray, red, green, brown, blue = (0,0,0), (255,255,255), (255,255,0), (128,128,128), (255,0,0), (0,255,0), (150,75,0), (40, 90, 200)

class Animal:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
        self.target_pos = pygame.Vector2(self.pos)
        self.speed = random.uniform(0.5, 1.5)
        self.move_timer = 0

    def update(self):
        self.move_timer -= 1
        if self.move_timer <= 0:
            angle = random.uniform(0, math.tau)
            dist = random.uniform(50, 150)
            self.target_pos = self.pos + pygame.Vector2(math.cos(angle) * dist, math.sin(angle) * dist)
            self.move_timer = random.randint(100, 300)

        move_dir = self.target_pos - self.pos
        if move_dir.length() > 2:
            self.pos += move_dir.normalize() * self.speed

    def draw(self, surface, cam_x, cam_y):
        pygame.draw.circle(surface, (255, 150, 150), (int(self.pos.x - cam_x), int(self.pos.y - cam_y)), 6)

# --- NOISE FUNCTIONS ---
def random_gradient(ix, iy):
    if (ix, iy) not in gradients:
        angle = random.random() * math.tau
        gradients[(ix, iy)] = (math.cos(angle), math.sin(angle))
    return gradients[(ix, iy)]

def dot_grid_gradient(ix, iy, x, y):
    gx, gy = random_gradient(ix, iy)
    return (x - ix) * gx + (y - iy) * gy

def fade(t): 
  return t * t * t * (t * (t * 6 - 15) + 10)
  
def lerp(a, b, t): 
  return a + t * (b - a)

def perlin(x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    x1, y1 = x0 + 1, y0 + 1
    sx, sy = fade(x - x0), fade(y - y0)
    n0, n1 = dot_grid_gradient(x0, y0, x, y), dot_grid_gradient(x1, y0, x, y)
    ix0 = lerp(n0, n1, sx)
    n0, n1 = dot_grid_gradient(x0, y1, x, y), dot_grid_gradient(x1, y1, x, y)
    ix1 = lerp(n0, n1, sx)
    return lerp(ix0, ix1, sy)

def tile_color(h):
    if h < WATER_LEVEL: return blue
    if h < SAND_LEVEL: return (220, 200, 120)
    if h < GRASS_LEVEL: return green
    if h < 0.6: return (30, 130, 60)
    return (120, 120, 120)

world_surface = pygame.Surface((world_w, world_h))

# --- GENERATION LOGIC ---
def spawn_logic_in_region(x_start, y_start, x_end, y_end):
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            h = perlin((x - offset_x) * SCALE, (y - offset_y) * SCALE)
            if h < WATER_LEVEL:
                if random.random() < 0.02:
                    animals.append(Animal(x, y))
            else:
                rand = random.random()
                if rand < 0.05: object_data[(x, y)] = "TREE"
                elif rand < 0.08: object_data[(x, y)] = "ROCK"
                elif rand < 0.09: animals.append(Animal(x, y))

def render_region(x_start, y_start, x_end, y_end, surf):
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            h = perlin((x - offset_x) * SCALE, (y - offset_y) * SCALE)
            draw_pos = (x * TILE_SIZE, y * TILE_SIZE)
            pygame.draw.rect(surf, (60, 180, 75), (*draw_pos, TILE_SIZE, TILE_SIZE))
            
            if h < WATER_LEVEL:
                pygame.draw.rect(surf, blue, (*draw_pos, TILE_SIZE, TILE_SIZE))
            elif h < SAND_LEVEL:
                pygame.draw.rect(surf, (220, 200, 120), (*draw_pos, TILE_SIZE, TILE_SIZE))
            else:
                surf.blit(grass_img, draw_pos)
            
            obj = object_data.get((x, y))
            if obj == "TREE":
                surf.blit(tree_img, draw_pos)
            elif obj == "ROCK":
                surf.blit(rock_img, draw_pos)

spawn_logic_in_region(0, 0, WIDTH, HEIGHT)
render_region(0, 0, WIDTH, HEIGHT, world_surface)

def expand_world(direction):
    global WIDTH, HEIGHT, world_w, world_h, world_surface, offset_x, offset_y, object_data
    
    if direction == "left":
        object_data = {(k[0] + CHUNK_SIZE, k[1]): v for k, v in object_data.items()}
        for a in animals: a.pos.x += CHUNK_SIZE * TILE_SIZE; a.target_pos.x += CHUNK_SIZE * TILE_SIZE
        offset_x += CHUNK_SIZE
        player_bx.x += (CHUNK_SIZE * TILE_SIZE)
    elif direction == "up":
        object_data = {(k[0], k[1] + CHUNK_SIZE): v for k, v in object_data.items()}
        for a in animals: a.pos.y += CHUNK_SIZE * TILE_SIZE; a.target_pos.y += CHUNK_SIZE * TILE_SIZE
        offset_y += CHUNK_SIZE
        player_bx.y += (CHUNK_SIZE * TILE_SIZE)

    if direction in ["left", "right"]: WIDTH += CHUNK_SIZE
    else: HEIGHT += CHUNK_SIZE
    
    world_w, world_h = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
    new_surf = pygame.Surface((world_w, world_h))
    new_surf.fill((60, 180, 75))
    if direction in ["right", "down"]: new_surf.blit(world_surface, (0, 0))
    elif direction == "left": new_surf.blit(world_surface, (CHUNK_SIZE * TILE_SIZE, 0))
    elif direction == "up": new_surf.blit(world_surface, (0, CHUNK_SIZE * TILE_SIZE))

    ranges = {
        "right": (WIDTH - CHUNK_SIZE, 0, WIDTH, HEIGHT),
        "left":  (0, 0, CHUNK_SIZE, HEIGHT),
        "down":  (0, HEIGHT - CHUNK_SIZE, WIDTH, HEIGHT),
        "up":    (0, 0, WIDTH, CHUNK_SIZE)
    }
    r = ranges[direction]
    spawn_logic_in_region(*r)
    render_region(0, 0, WIDTH, HEIGHT, new_surf) 

    world_surface = new_surf

while running:
    dt = clock.get_time() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    keys = pygame.key.get_pressed()
    is_sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] and sprint_width > 2
    curr_speed = 7 if is_sprinting else 4
    if is_sprinting: sprint_width -= 2
    elif sprint_width < 250: sprint_width += stamina_regen

    move = pygame.Vector2(0,0)
    if keys[pygame.K_a]: move.x -= 1
    if keys[pygame.K_d]: move.x += 1
    if keys[pygame.K_w]: move.y -= 1
    if keys[pygame.K_s]: move.y += 1
    if move.length() > 0: player_bx.topleft += move.normalize() * curr_speed

    BUF = 150
    if player_bx.right > world_w - BUF: expand_world("right")
    if player_bx.left < BUF: expand_world("left")
    if player_bx.bottom > world_h - BUF: expand_world("down")
    if player_bx.top < BUF: expand_world("up")

    for a in animals: 
      a.update()

    cam_x, cam_y = player_bx.centerx - SCREEN_W//2, player_bx.centery - SCREEN_H//2
    
    screen.fill(black)
    screen.blit(world_surface, (-cam_x, -cam_y))
    
    for a in animals:
      a.draw(screen, cam_x, cam_y)

    pygame.draw.rect(screen, red, (player_bx.x - cam_x, player_bx.y - cam_y, player_bx.w, player_bx.h))
    pygame.draw.rect(screen, gray, (10, 10, 250, 15))
    pygame.draw.rect(screen, yellow, (10, 10, max(0, sprint_width), 15))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

