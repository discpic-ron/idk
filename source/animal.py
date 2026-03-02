class Animal:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
        self.target_pos = pygame.Vector2(self.pos)
        self.speed = random.uniform(0.5, 1.5)
        self.move_timer = 0
        self.max_health = 100
        self.health = self.max_health
        
    def takeDamage(self,amount):
        self.health -= amount
        
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
