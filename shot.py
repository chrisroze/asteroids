import pygame
from circleshape import CircleShape 
from constants import SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=SHOT_RADIUS)
        self.velocity = PLAYER_SHOOT_SPEED * pygame.Vector2(1, 0)  # Initial velocity to the right, will be rotated by player direction
        self._color_cycle = [
            (255, 255, 0),  # yellow
            (255, 230, 0),
            (255, 205, 0),
            (255, 180, 0),
            (255, 155, 0),
            (255, 130, 0),
            (255, 105, 0),
            (255, 80, 0),
            (255, 55, 0),
            (255, 30, 0),  # near-red/orange to red
        ]
        self._color_index = 0
        self._color_direction = 1  # 1 = forward, -1 = backward

    def draw(self, screen):
        color = self._color_cycle[self._color_index]
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        # Ping-pong color cycling
        self._color_index += self._color_direction
        if self._color_index >= len(self._color_cycle):
            self._color_index = len(self._color_cycle) - 2
            self._color_direction = -1
        elif self._color_index < 0:
            self._color_index = 1
            self._color_direction = 1

        self.position += self.velocity * dt

        # Remove shot when it exits screen bounds
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()