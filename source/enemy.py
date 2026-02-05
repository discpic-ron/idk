import math,pygame
class Enemy:
    def __init__(self, health, size, x, y, speed=2):
        self.max_health = health
        self.health = health
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.is_dead = False

    def update(self, target_x, target_y):
        # Move toward player
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, surface, camera_x, camera_y):
        enemy_rect = pygame.Rect(self.x - camera_x, self.y - camera_y, self.size, self.size)
        pygame.draw.rect(surface, (0, 0, 255), enemy_rect)

        # Health bar
        bar_w = self.size
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (self.x - camera_x, self.y - 10 - camera_y, bar_w, 5))
        pygame.draw.rect(surface, (0, 255, 0),(self.x - camera_x, self.y - 10 - camera_y, int(bar_w * health_ratio), 5))

        return enemy_rect
