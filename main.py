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
from particle import Particle, FloatingText

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")


def main():
    start_time = time.time()
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print(f"Game start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    pygame.init()
    dt = 0
    score = 0

    clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroid_field = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    font = pygame.font.SysFont(None, 30)
    pause_font = pygame.font.SysFont('comicsansms', 60, bold=True)
    stage_msg_font = pygame.font.SysFont('comicsansms', 72, bold=True)
    stage_message = ""
    stage_message_timer = 0.0
    current_stage = 1

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (asteroid_field, updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)
    FloatingText.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    asteroid_field = AsteroidField()
    asteroid_field.spawn_rate = ASTEROID_SPAWN_RATE_SECONDS

    paused = False

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Game exited by user.")
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
                log_event("pause_toggled")

        if not paused:
            updatable.update(dt)

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
                        for _ in range(10):
                            Particle(shot.position.x, shot.position.y)
                        asteroid_killed = asteroid.split()
                        shot.kill()

                        if asteroid_killed:
                            score += 15
                            FloatingText(asteroid.position.x, asteroid.position.y, "15", color=(255, 215, 0), lifetime=1.1)
                        else:
                            score += 10
                            FloatingText(asteroid.position.x, asteroid.position.y, "10", color=(173, 216, 230), lifetime=1.1)

            level = score // 200
            stage = 1 + level
            if stage != current_stage:
                current_stage = stage
                player.stage = stage
                asteroid_field.stage = stage
                stage_message = f"Stage {stage}"
                stage_message_timer = 1.5
                log_event("stage_up")

            if stage < 4:
                player.shoot_cooldown = max(0.1, PLAYER_SHOOT_COOLDOWN_SECONDS - 0.1 * level)
                asteroid_field.spawn_rate = max(0.1, ASTEROID_SPAWN_RATE_SECONDS - 0.2 * level)
            else:
                player.shoot_cooldown = max(0.1, PLAYER_SHOOT_COOLDOWN_SECONDS - 0.05 * level + 0.1)
                asteroid_field.spawn_rate = max(0.1, ASTEROID_SPAWN_RATE_SECONDS - 0.4 * level)
        else:
            level = score // 200
            stage = 1 + level
            player.stage = stage

        if stage_message_timer > 0:
            stage_message_timer = max(0.0, stage_message_timer - dt)

        screen.fill((0, 0, 0))
        for obj in drawable:
            obj.draw(screen)

        if paused:
            paused_surface = pause_font.render("Paused", True, (255, 0, 0))
            paused_rect = paused_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(paused_surface, paused_rect)
        else:
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

        if stage_message_timer > 0 and stage_message:
            alpha = int(255 * (stage_message_timer / 1.5))
            alpha = max(40, min(255, alpha))  # minimum visibility
            stage_surface = stage_msg_font.render(stage_message, True, (255, 255, 0))
            stage_surface.set_alpha(alpha)
            stage_rect = stage_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(stage_surface, stage_rect)

        pygame.display.flip()

        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()
