from logger import log_event
from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, ASTEROID_KINDS
import pygame
import random   
import math

class Asteroid(CircleShape):
    @staticmethod
    def radius_for_kind(kind):
        kind = max(1, min(ASTEROID_KINDS, int(kind)))
        if ASTEROID_KINDS <= 1:
            return ASTEROID_MIN_RADIUS
        step = (ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS) / (ASTEROID_KINDS - 1)
        return int(ASTEROID_MIN_RADIUS + (kind - 1) * step)

    def __init__(self, x, y, radius=None, kind=1, velocity=200, fill_color=None):
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

        if fill_color is None:
            # random fill color (full RGB range)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.fill_color = (r, g, b)
        else:
            self.fill_color = fill_color
        self.outline_width = LINE_WIDTH + 7
        self.gradient_surface = self._create_gradient_surface()
        self.outline_gradient_surface = self._create_outline_gradient_surface()

    def _create_gradient_surface(self):
        diameter = self.radius * 2
        gradient_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (self.radius, self.radius)

        for current_radius in range(self.radius, 0, -1):
            blend = (current_radius / self.radius) ** 1.8
            color = (
                int(255 + (self.fill_color[0] - 255) * blend),
                int(255 + (self.fill_color[1] - 255) * blend),
                int(255 + (self.fill_color[2] - 255) * blend),
            )
            pygame.draw.circle(gradient_surface, color, center, current_radius)

        return gradient_surface

    def _create_outline_gradient_surface(self):
        margin = self.outline_width + 2
        diameter = (self.radius + margin) * 2
        outline_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (self.radius + margin, self.radius + margin)

        inner_radius = max(1, self.radius - (self.outline_width // 2))
        outer_radius = self.radius + ((self.outline_width + 1) // 2)
        ring_width = max(1.0, float(outer_radius - inner_radius))

        for y in range(diameter):
            for x in range(diameter):
                dist = math.hypot(x - center[0], y - center[1])

                if inner_radius <= dist <= outer_radius:
                    blend = (dist - inner_radius) / ring_width
                    color = (
                        int(self.fill_color[0] * (1 - blend)),
                        int(self.fill_color[1] * (1 - blend)),
                        int(self.fill_color[2] * (1 - blend)),
                        255,
                    )
                    outline_surface.set_at((x, y), color)
                elif inner_radius - 1.0 <= dist < inner_radius:
                    alpha = int(255 * (dist - (inner_radius - 1.0)))
                    outline_surface.set_at((x, y), (*self.fill_color, alpha))
                elif outer_radius < dist <= outer_radius + 1.0:
                    alpha = int(255 * (1.0 - (dist - outer_radius)))
                    outline_surface.set_at((x, y), (0, 0, 0, alpha))

        return outline_surface

    def draw(self, screen):
        # Draw asteroid with radial gradient (white center -> selected edge color).
        screen.blit(
            self.gradient_surface,
            (int(self.position.x - self.radius), int(self.position.y - self.radius)),
        )
        outline_offset = self.radius + self.outline_width
        screen.blit(
            self.outline_gradient_surface,
            (int(self.position.x - outline_offset), int(self.position.y - outline_offset)),
        )

    def split(self):
        self.kill()  # Remove the original asteroid
        # If asteroid is minimum size, it is fully destroyed
        if self.radius <= ASTEROID_MIN_RADIUS:
            log_event("asteroid_destroyed")
            return True

        # Otherwise split into two smaller asteroids
        log_event("asteroid_split")
        new_kind = max(1, self.kind - 1)
        new_radius = self.radius_for_kind(new_kind)

        angle = random.uniform(20, 50)  # Split angle between 20 and 50 degrees
        velocity1 = self.velocity.rotate(angle) * random.uniform(0.8, 1.2)
        velocity2 = self.velocity.rotate(-angle) * random.uniform(0.8, 1.2)

        Asteroid(
            self.position.x,
            self.position.y,
            radius=new_radius,
            kind=new_kind,
            velocity=velocity1,
            fill_color=self.fill_color,
        )
        Asteroid(
            self.position.x,
            self.position.y,
            radius=new_radius,
            kind=new_kind,
            velocity=velocity2,
            fill_color=self.fill_color,
        )

        return False


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