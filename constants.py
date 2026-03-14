# Constants for the Asteroids game
# This file defines various constants used throughout the game, such as screen dimensions, player properties, and drawing parameters. Centralizing these values makes it easier to adjust game settings and maintain consistency across different modules.

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player properties
PLAYER_RADIUS = 20 # Radius of the player's circular hitbox
LINE_WIDTH = 2 # Thickness of lines for drawing shapes
PLAYER_TURN_SPEED = 300  # Degrees per second
PLAYER_SPEED = 200  # Pixels per second

# Asteroid properties
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Shot properties
SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3