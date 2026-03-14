import pygame
import random   
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE_SECONDS

class AsteroidField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0

    def spawn_asteroid(self, x, y, kind=None, velocity=None):
        if kind is None:
            kind = random.randint(1, ASTEROID_KINDS)

        radius = Asteroid.radius_for_kind(kind)
        if velocity is None:
            velocity = pygame.Vector2(random.uniform(-200, 200), random.uniform(-200, 200))

        asteroid = Asteroid(x, y, radius=radius, kind=kind, velocity=velocity)
        # self.containers.add(asteroid)

    def _spawn_edge_position(self):
        edge_thickness = int(min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.15)
        side = random.choice(['left', 'right', 'top', 'bottom'])

        if side == 'left':
            x = random.randint(0, edge_thickness)
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 'right':
            x = random.randint(SCREEN_WIDTH - edge_thickness, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, edge_thickness)
        else:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT - edge_thickness, SCREEN_HEIGHT)

        return x, y

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0
            x, y = self._spawn_edge_position()
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn_asteroid(x, y, kind=kind)

