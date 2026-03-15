import sys

from shot import Shot
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import math

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS * 0.8)  # Circle hitbox is smaller than visual triangle for better gameplay feel
        self.rotation = 0
        self.shot_timer = 0  # Cooldown timer for shooting, in seconds
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.stage = 1

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
        points = self.triangle()
        # Draw solid blueish player shape and then outline with configured width.
        pygame.draw.polygon(screen, (100, 150, 255), points)
        pygame.draw.polygon(screen, (255, 255, 255), points, LINE_WIDTH )

    def rotate(self, dt):
        # Rotate player by configured turn speed. Rotation is in degrees
        self.rotation += PLAYER_TURN_SPEED * dt 

    def move(self, dt):
        # Move player forward in the direction they are currently facing.
        angle = math.radians(self.rotation)
        direction = pygame.Vector2(math.sin(angle), -math.cos(angle))
        self.position += direction * PLAYER_SPEED * dt
        # Wrap around screen edges        
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH    
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT 

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
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)

        if keys[pygame.K_RIGHT]:
            self.rotate(+dt)

        # Handle player input for movement. Up arrow moves forward, down arrow moves backward.
        if keys[pygame.K_UP]:
            self.move(+dt)   
        
        if keys[pygame.K_DOWN]:
            self.move(-dt)

        if keys[pygame.K_ESCAPE]:
            print("Game exited by user.")
            pygame.quit()
            sys.exit()

#   Handle player input for shooting. Space bar creates a new shot object with velocity in the direction the player is facing.
        # if keys[pygame.K_SPACE]:
        self.shoot(dt)
