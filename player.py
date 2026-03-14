from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_TURN_SPEED
import pygame
import math

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

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
        pygame.draw.polygon(screen, (255, 255, 255), points, LINE_WIDTH)

    def rotate(self, dt):
        # Rotate player by configured turn speed. Rotation is in degrees
        self.rotation += PLAYER_TURN_SPEED * dt 

    def move(self, dt):
        # Move player forward in the direction they are currently facing.
        angle = math.radians(self.rotation)
        direction = pygame.Vector2(math.sin(angle), -math.cos(angle))
        self.position += direction * PLAYER_SPEED * dt

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
