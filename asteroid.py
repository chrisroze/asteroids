from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_KINDS
import pygame
import random   

class Asteroid(CircleShape):
    @staticmethod
    def radius_for_kind(kind):
        kind = max(1, min(ASTEROID_KINDS, int(kind)))
        if ASTEROID_KINDS <= 1:
            return ASTEROID_MIN_RADIUS
        step = (ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS) / (ASTEROID_KINDS - 1)
        return int(ASTEROID_MIN_RADIUS + (kind - 1) * step)

    def __init__(self, x, y, radius=None, kind=1, velocity=200):
        if kind is None:
            kind = 1
        kind = max(1, min(ASTEROID_KINDS, int(kind)))

        if radius is None:
            radius = self.radius_for_kind(kind)
        else:
            # if a custom radius is provided, determine closest kind
            closest_kind = round((radius - ASTEROID_MIN_RADIUS) / max(1, (ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS)) * (ASTEROID_KINDS - 1)) + 1
            kind = max(1, min(ASTEROID_KINDS, closest_kind))
            radius = self.radius_for_kind(kind)

        super().__init__(x, y, radius)
        self.kind = kind
        self.velocity = velocity

        # random brown-like fill color
        r = random.randint(130, 200)
        g = random.randint(70, 130)
        b = random.randint(30, 90)
        self.fill_color = (r, g, b)
        # darker outline for contrast
        self.outline_color = (max(0, r - 30), max(0, g - 30), max(0, b - 30))

    def draw(self, screen):
        # Draw random brown asteroid shape and darker outline.
        pygame.draw.circle(screen, self.fill_color, self.position, self.radius)
        pygame.draw.circle(screen, self.outline_color, self.position, self.radius, LINE_WIDTH)

    def split(self):
        self.kill()  # Remove the original asteroid
        # Split asteroid into two smaller ones if it's above minimum size
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []  # Too small to split, just destroy
        
        log_event("asteroid_split") # Log the split event
        new_kind = max(1, self.kind - 1)
        new_radius = self.radius_for_kind(new_kind)

        # Create two new asteroids with slightly different velocities
        angle = random.uniform(20, 50)  # Split angle between 20 and 50 degrees
        velocity1 = self.velocity.rotate(angle) * random.uniform(0.8, 1.2)
        velocity2 = self.velocity.rotate(-angle) * random.uniform(0.8, 1.2)

        asteroid1 = Asteroid(self.position.x, self.position.y, radius=new_radius, kind=new_kind, velocity=velocity1)
        asteroid2 = Asteroid(self.position.x, self.position.y, radius=new_radius, kind=new_kind, velocity=velocity2)

        return


    def update(self, dt):
        # Move asteroid based on its velocity and delta time
        self.position += self.velocity * dt
        # Wrap around screen edges        
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH    
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT            