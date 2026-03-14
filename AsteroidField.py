import pygame
import random   
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_SPAWN_RATE_SECONDS

class AsteroidField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0

    def spawn_asteroid(self, x, y, radius, velocity):
        asteroid = Asteroid(x, y, radius, velocity)
        # self.containers.add(asteroid)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
            velocity = pygame.Vector2(random.uniform(-200, 200), random.uniform(-200, 200))
            self.spawn_asteroid(x, y, radius, velocity)


