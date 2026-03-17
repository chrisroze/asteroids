#   Asteroids Game
#   A simple implementation of the classic Asteroids game using Pygame.
#   This code sets up the game window, initializes the player and asteroids, and handles
#   the main game loop, including event handling, updating game objects, and rendering.
#   The game features a player-controlled spaceship that can move and rotate, and a field of asteroids
#   that the player must avoid. The game ends when the player collides with an asteroid.

import sys
import time
import random
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


def quit_game():
    # Cleanly exit the game and close pygame.
    log_event("Game exited by user.")
    pygame.quit()
    sys.exit()


def handle_title(screen, clock, stars, title_letter_surfaces, title_total_width, title_hint_font):
    # Run the title menu loop until the player starts or quits.
    # Keep showing the title screen until Enter starts or Escape quits.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return

        screen.fill((0, 0, 0))
        for x, y, radius, color in stars:
            pygame.draw.circle(screen, color, (x, y), radius)

        current_x = (SCREEN_WIDTH - title_total_width) / 2
        title_y = (SCREEN_HEIGHT / 2) - 80
        for letter_surface in title_letter_surfaces:
            screen.blit(letter_surface, (current_x, title_y))
            current_x += letter_surface.get_width()

        enter_surface = title_hint_font.render("Press Enter to Play", True, (255, 255, 255))
        enter_rect = enter_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 15))
        screen.blit(enter_surface, enter_rect)

        escape_surface = title_hint_font.render("Press Escape to Quit", True, (255, 255, 255))
        escape_rect = escape_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 55))
        screen.blit(escape_surface, escape_rect)

        pygame.display.flip()
        clock.tick(60)


def handle_pause(screen, pause_font):
    # Draw the paused overlay text.
    paused_surface = pause_font.render("Paused", True, (255, 0, 0))
    paused_rect = paused_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(paused_surface, paused_rect)


def handle_game_over(screen, game_over_font, game_over_hint_font, score, highest_stage):
    # Draw the game-over overlay and restart/quit prompts.
    game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    game_over_surface.fill((0, 0, 0, 170))
    screen.blit(game_over_surface, (0, 0))

    over_text = game_over_font.render("Game Over", True, (255, 80, 80))
    over_rect = over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(over_text, over_rect)

    final_score_text = game_over_hint_font.render(f"Final Score: {score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 5))
    screen.blit(final_score_text, final_score_rect)

    highest_stage_text = game_over_hint_font.render(f"Stage: {highest_stage}", True, (255, 255, 255))
    highest_stage_rect = highest_stage_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30))
    screen.blit(highest_stage_text, highest_stage_rect)

    restart_text = game_over_hint_font.render("Press Enter to start a new game", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 75))
    screen.blit(restart_text, restart_rect)

    quit_text = game_over_hint_font.render("Press Escape to quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110))
    screen.blit(quit_text, quit_rect)


def handle_playing(updatable, asteroids, player, shots, asteroid_field, dt, score, current_stage, highest_stage, stage_message, stage_message_timer):
    # Update active gameplay, collisions, scoring, and stage progression.
    game_over = False
    updatable.update(dt)

    for asteroid in asteroids:
        if player.collide_with(asteroid):
            log_event("player_hit")
            print("Player collided with an asteroid! Game Over.")
            game_over = True
            break

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
    highest_stage = max(highest_stage, stage)
    if stage != current_stage:
        current_stage = stage
        player.stage = stage
        asteroid_field.stage = stage
        stage_message = f"Stage {stage}"
        stage_message_timer = 1.5
        log_event("stage_up")

#   Adjust difficulty by modifying player shoot cooldown and asteroid spawn rate based on the current stage.
    if stage < 4:
        player.shoot_cooldown = max(0.1, PLAYER_SHOOT_COOLDOWN_SECONDS - 0.1 * level)
        asteroid_field.spawn_rate = max(0.1, ASTEROID_SPAWN_RATE_SECONDS - 0.2 * level)
    else:
        player.shoot_cooldown = max(0.1, PLAYER_SHOOT_COOLDOWN_SECONDS - 0.05 * level + 0.05)
        asteroid_field.spawn_rate = max(0.3, ASTEROID_SPAWN_RATE_SECONDS - 0.3 * level)

    return score, game_over, stage, current_stage, highest_stage, stage_message, stage_message_timer


def reset_game_state():
    # Initialize and return all state needed for a fresh run.
    start_time = time.time()
    print(f"Game start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    dt = 0
    score = 0
    stage_message = ""
    stage_message_timer = 0.0
    current_stage = 1
    stage = 1
    highest_stage = 1
    game_over = False
    paused = False
    restart_requested = False

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroid_field_group = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (asteroid_field_group, updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)
    FloatingText.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    asteroid_field = AsteroidField()
    asteroid_field.spawn_rate = ASTEROID_SPAWN_RATE_SECONDS

    return (
        start_time, dt, score, stage_message, stage_message_timer, current_stage,
        stage, highest_stage, game_over, paused, restart_requested,
        updatable, drawable, asteroids, shots, player, asteroid_field,
    )


def main():
    # Configure resources and run the main game/restart loops.
    print("Starting Asteroids with pygame version:", pygame.version.ver)

    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    pause_font = pygame.font.SysFont('comicsansms', 60, bold=True)
    stage_msg_font = pygame.font.SysFont('comicsansms', 72, bold=True)
    game_over_font = pygame.font.SysFont('comicsansms', 80, bold=True)
    game_over_hint_font = pygame.font.SysFont(None, 42)
    title_font = pygame.font.SysFont('comicsansms', 110, bold=True)
    title_hint_font = pygame.font.SysFont(None, 46)

    star_count = 180
    star_colors = [
        (255, 255, 255),
        (220, 235, 255),
        (255, 245, 210),
        (200, 220, 255),
    ]
    stars = [
        (
            random.randint(0, SCREEN_WIDTH - 1),
            random.randint(0, SCREEN_HEIGHT - 1),
            random.choice([1, 1, 1, 2, 2, 3]),
            random.choice(star_colors),
        )
        for _ in range(star_count)
    ]

    title_letters = list("ASTEROIDS")
    title_letter_surfaces = [
        title_font.render(
            letter,
            True,
            (
                random.randint(70, 255),
                random.randint(70, 255),
                random.randint(70, 255),
            ),
        )
        for letter in title_letters
    ]
    title_total_width = sum(surface.get_width() for surface in title_letter_surfaces)

    handle_title(screen, clock, stars, title_letter_surfaces, title_total_width, title_hint_font)

    # Start a new game session each time the player chooses restart.
    while True:
        (
            start_time, dt, score, stage_message, stage_message_timer, current_stage,
            stage, highest_stage, game_over, paused, restart_requested,
            updatable, drawable, asteroids, shots, player, asteroid_field,
        ) = reset_game_state()

        # Run one frame per iteration until a restart is requested or quit is triggered.
        while True:
            log_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_ESCAPE:
                            quit_game()
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            restart_requested = True
                            log_event("game_restarted")
                    else:
                        if event.key == pygame.K_ESCAPE:
                            quit_game()
                        if event.key == pygame.K_SPACE:
                            paused = not paused
                            log_event("pause_toggled")

            if restart_requested:
                break

            if not paused and not game_over:
                score, game_over, stage, current_stage, highest_stage, stage_message, stage_message_timer = handle_playing(
                    updatable, asteroids, player, shots, asteroid_field, dt,
                    score, current_stage, highest_stage, stage_message, stage_message_timer
                )
                if game_over:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    print(f"Game end time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
                    print(f"Total runtime: {elapsed:.2f} seconds")
                    print(f"Final score: {score} points")
                    paused = False
            else:
                level = score // 200
                stage = 1 + level
                highest_stage = max(highest_stage, stage)
                player.stage = stage

            if stage_message_timer > 0:
                stage_message_timer = max(0.0, stage_message_timer - dt)

            screen.fill((0, 0, 0))
            for x, y, radius, color in stars:
                pygame.draw.circle(screen, color, (x, y), radius)

            for obj in drawable:
                obj.draw(screen)

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

            if paused and not game_over:
                handle_pause(screen, pause_font)

            if stage_message_timer > 0 and stage_message and not game_over:
                alpha = int(255 * (stage_message_timer / 1.5))
                alpha = max(40, min(255, alpha))  # minimum visibility
                stage_surface = stage_msg_font.render(stage_message, True, (255, 255, 0))
                stage_surface.set_alpha(alpha)
                stage_rect = stage_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(stage_surface, stage_rect)

            if game_over:
                handle_game_over(screen, game_over_font, game_over_hint_font, score, highest_stage)

            pygame.display.flip()

            dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()
