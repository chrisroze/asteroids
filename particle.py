import random
import pygame
from circleshape import CircleShape


def lerp_color(color_a, color_b, t):
    return (
        int(color_a[0] + (color_b[0] - color_a[0]) * t),
        int(color_a[1] + (color_b[1] - color_a[1]) * t),
        int(color_a[2] + (color_b[2] - color_a[2]) * t),
    )


class Particle(CircleShape):
    def __init__(self, x, y, lifetime=1.0):
        super().__init__(x, y, radius=random.randint(2, 4))
        self.lifetime = lifetime
        self.age = 0.0

        # Random outward velocity vector
        direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        self.velocity = direction.normalize() * random.uniform(120, 260)

        # Color gradient from yellow to red
        gradient_pos = random.random()
        self.color = lerp_color((255, 255, 0), (255, 0, 0), gradient_pos)

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return

        # Move particle outward
        self.position += self.velocity * dt

        # Optional fade-out (not required but looks nice)
        fade = max(0, 1.0 - self.age / self.lifetime)
        self.color = (
            int(self.color[0] * fade),
            int(self.color[1] * fade),
            int(self.color[2] * fade),
        )

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
