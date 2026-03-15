import sys

from shot import Shot
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_DECELERATION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
import pygame
import math
import random

class Player(CircleShape):
    @staticmethod
    def _luminance(color):
        return (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2])

    @staticmethod
    def _color_distance(color_a, color_b):
        return math.sqrt(
            (color_a[0] - color_b[0]) ** 2
            + (color_a[1] - color_b[1]) ** 2
            + (color_a[2] - color_b[2]) ** 2
        )

    @classmethod
    def _random_bright_color(cls, min_luminance=170):
        while True:
            color = (
                random.randint(90, 255),
                random.randint(90, 255),
                random.randint(90, 255),
            )
            if cls._luminance(color) >= min_luminance:
                return color

    @classmethod
    def _random_player_colors(cls):
        fill_color = cls._random_bright_color(min_luminance=165)

        for _ in range(50):
            outline_color = cls._random_bright_color(min_luminance=185)
            if cls._color_distance(fill_color, outline_color) >= 120:
                return fill_color, outline_color

        return fill_color, (255, 255, 255)

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS * 0.8)  # Circle hitbox is smaller than visual triangle for better gameplay feel
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.shot_timer = 0  # Cooldown timer for shooting, in seconds
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.stage = 1
        self.thrusting = False
        self.fill_color, self.outline_color = self._random_player_colors()

    def triangle(self):
        # Isosceles triangle centered on player position, sized by radius
        # Base is ~30% shorter than equilateral base.
        angle = math.radians(self.rotation)
        offsets = [
            pygame.Vector2(0, -self.radius),
            pygame.Vector2(self.radius * 0.6, self.radius * 0.5),
            pygame.Vector2(-self.radius * 0.6, self.radius * 0.5),
        ]

        points = [(self.position + off.rotate_rad(angle)).xy for off in offsets]
        return points

    def draw(self, screen):
        # Circle hitbox exists in physics state (self.position and self.radius),
        # but it is intentionally not drawn. This keeps collision logic separate
        # from visual representation.
        if self.thrusting:
            angle = math.radians(self.rotation)
            forward = pygame.Vector2(math.sin(angle), -math.cos(angle))
            right = pygame.Vector2(-forward.y, forward.x)
            flame_base = self.position - forward * (self.radius * 0.5)
            flame_offset = self.radius * 0.3

            for side in (-1, 1):
                center = flame_base + right * flame_offset * side
                flame_surface = pygame.Surface((12, 8), pygame.SRCALPHA)
                pygame.draw.ellipse(flame_surface, (255, 140, 40), flame_surface.get_rect())
                rotated = pygame.transform.rotate(flame_surface, -self.rotation)
                flame_rect = rotated.get_rect(center=(center.x, center.y))
                screen.blit(rotated, flame_rect)

        points = self.triangle()
        pygame.draw.polygon(screen, self.fill_color, points)
        pygame.draw.polygon(screen, self.outline_color, points, LINE_WIDTH)

    def rotate(self, dt):
        # Rotate player by configured turn speed. Rotation is in degrees
        self.rotation += PLAYER_TURN_SPEED * dt 

    def _wrap_position(self):
        # Wrap around screen edges        
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH    
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT 

    def _apply_movement(self, dt):
        self.position += self.velocity * dt
        self._wrap_position()

    def shoot(self, dt):
        # Create a new shot object and set its velocity based on the player's current rotation
        if self.shot_timer > 0:
            self.shot_timer -= dt
            return  # Still in cooldown, cannot shoot

        shot = Shot(self.position.x, self.position.y)
        angle = math.radians(self.rotation)
        forward_velocity = PLAYER_SHOOT_SPEED * pygame.Vector2(math.sin(angle), -math.cos(angle))
        shot.velocity = forward_velocity

        # stage 4+ (score >= 800) spawns a backward shot too
        if self.stage >= 4:
            back_shot = Shot(self.position.x, self.position.y)
            back_shot.velocity = -forward_velocity

        self.shot_timer = self.shoot_cooldown  # Reset cooldown timer

    def update(self, dt):
        # Handle player input for rotation. Left and right arrow keys rotate the player.
        keys = pygame.key.get_pressed()
        angle = math.radians(self.rotation)
        direction = pygame.Vector2(math.sin(angle), -math.cos(angle))

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)

        if keys[pygame.K_RIGHT]:
            self.rotate(+dt)

        # Up arrow applies thrust up to max speed. Releasing it decelerates gradually.
        self.thrusting = keys[pygame.K_UP]
        if keys[pygame.K_UP]:
            self.velocity += direction * PLAYER_ACCELERATION * dt
            if self.velocity.length_squared() > PLAYER_SPEED * PLAYER_SPEED:
                self.velocity.scale_to_length(PLAYER_SPEED)
        else:
            speed = self.velocity.length()
            if speed > 0:
                speed = max(0.0, speed - PLAYER_DECELERATION * dt)
                if speed == 0:
                    self.velocity = pygame.Vector2(0, 0)
                else:
                    self.velocity.scale_to_length(speed)

        if keys[pygame.K_DOWN]:
            self.position += (-direction) * (PLAYER_SPEED * 0.5) * dt

        self._apply_movement(dt)

        if keys[pygame.K_ESCAPE]:
            print("Game exited by user.")
            pygame.quit()
            sys.exit()

#   Handle player input for shooting. Space bar creates a new shot object with velocity in the direction the player is facing.
        # if keys[pygame.K_SPACE]:
        self.shoot(dt)
