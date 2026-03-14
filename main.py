#   Asteroids Game
#   A simple implementation of the classic Asteroids game using Pygame.
#   This code sets up the game window, initializes the player and asteroids, and handles
#   the main game loop, including event handling, updating game objects, and rendering.
#   The game features a player-controlled spaceship that can move and rotate, and a field of asteroids
#   that the player must avoid. The game ends when the player collides with an asteroid.

import sys
import time
import pygame
from shot import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SHOOT_COOLDOWN_SECONDS, ASTEROID_SPAWN_RATE_SECONDS
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from AsteroidField import AsteroidField

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")


def main():
    # Log game start time and pygame version
    start_time = time.time()
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print(f"Game start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
#    print(f"Screen width: {SCREEN_WIDTH}")
#    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame and set up the game window
    pygame.init()
    dt = 0 
    score = 0

    # Set up game objects and groups
    clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroid_field = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Font for UI text
    font = pygame.font.SysFont(None, 30)

    # Set the containers for each class
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (asteroid_field, updatable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
    asteroid_field = AsteroidField()
    asteroid_field.spawn_rate = ASTEROID_SPAWN_RATE_SECONDS
    # ast1 = Asteroid(100, 100, 30, velocity=pygame.Vector2(50, 30))
    # ast2 = Asteroid(300, 200, 40, velocity=pygame.Vector2(-200, 200))
    

    # Create multiple asteroids in the field with random positions and velocities
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Game exited by user.")
                pygame.quit()
                return
        # Update game objects
        updatable.update(dt)

        # Check for collisions between player and asteroids and log the event if it occurs and end the game 
        for asteroid in asteroids:
            if player.collide_with(asteroid):
                log_event("player_hit")
                print("Player collided with an asteroid! Game Over.")
                end_time = time.time()
                elapsed = end_time - start_time
                print(f"Game end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
                print(f"Total runtime: {elapsed:.2f} seconds")
                print(f"Final score: {score} points")
                sys.exit()
            for shot in shots:
                if shot.collide_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()  # Split asteroid into smaller ones if it's above minimum size
                    shot.kill()  # Remove the shot
                    score += 10  # Increment score for hitting an asteroid

        # Difficulty scaling: every 200 points
        level = score // 200
        player.shoot_cooldown = max(0.1, PLAYER_SHOOT_COOLDOWN_SECONDS - 0.1 * level)
        asteroid_field.spawn_rate = max(0.5, ASTEROID_SPAWN_RATE_SECONDS - 0.3 * level)
        stage = min(5, 1 + level)

        # Update the display with the new positions of the player and asteroids and log the frame update event
        screen.fill((0, 0, 0))  # Clear the screen with black
        for obj in drawable:
            obj.draw(screen)  # Call the custom draw method for each object

        # Update scoreboard text and draw top-center in white
        stage_text = f"Stage: {stage}"
        title_text = f"Score: {score}"
        asteroid_count_text = f"Asteroids: {len(asteroids)}"

        stage_surface = font.render(stage_text, True, (255, 255, 255))
        stage_rect = stage_surface.get_rect(midtop=(SCREEN_WIDTH / 2, 10))
        screen.blit(stage_surface, stage_rect)

        title_surface = font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(midtop=(SCREEN_WIDTH / 2, stage_rect.bottom + 5))
        screen.blit(title_surface, title_rect)

        count_surface = font.render(asteroid_count_text, True, (255, 255, 255))
        count_rect = count_surface.get_rect(midtop=(SCREEN_WIDTH / 2, title_rect.bottom + 5))
        screen.blit(count_surface, count_rect)

        pygame.display.flip()  # Update the display

        # Limit to 60 frames per second and get delta time in seconds
        dt = clock.tick(60) / 1000.0  # Limit to 60 frames per second and get delta time in seconds
        


if __name__ == "__main__":
    main()
