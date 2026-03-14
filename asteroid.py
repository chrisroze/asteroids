from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import random   

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=200):
        super().__init__(x, y, radius)
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