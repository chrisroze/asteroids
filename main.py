import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from AsteroidField import AsteroidField

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")


def main():
    print("Starting Asteroids with pygame version: ", pygame.version.ver)
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    delta_rotation = 0  
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroid_field = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (asteroid_field, updatable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()
    # ast1 = Asteroid(100, 100, 30, velocity=pygame.Vector2(50, 30))
    # ast2 = Asteroid(300, 200, 40, velocity=pygame.Vector2(-200, 200))
    


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log_event("Game exited by user.")
                pygame.quit()
                return
        # Update and draw player
        updatable.update(dt)

        #update the display
        screen.fill((0, 0, 0))  # Clear the screen with black
#        drawable.draw(screen)
        for obj in drawable:
            obj.draw(screen)  # Call the custom draw method for each object

        pygame.display.flip()  # Update the display

        # Limit to 60 frames per second and get delta time in seconds
        dt = clock.tick(60) / 1000.0  # Limit to 60 frames per second and get delta time in seconds
        # print(f"Delta time (seconds): {dt:.4f}")

if __name__ == "__main__":
    main()
