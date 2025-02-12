import pygame
from pygame.math import Vector2
import math
import random
from asteroid import Asteroid
from spaceship import Spaceship
from osd import OSD


# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1280
halfx = SCREEN_WIDTH // 2
halfy = SCREEN_HEIGHT // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")
world_radius = 15000
running = True


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():
    ship = Spaceship(0, 0)
    all_asteroids = []
    for i in range(15000):
        radius = world_radius * math.sqrt(random.random())
        alpha = random.uniform(0, 2 * math.pi)
        x = radius * math.cos(alpha)
        y = radius * math.sin(alpha)
        one_asteroid = Asteroid(x, y, random.randint(15, 90))
        all_asteroids.append(one_asteroid)

    totalasteroids = len(all_asteroids)

    clock = pygame.time.Clock()
    osd = OSD(screen)

    global running
    screenhalfx = screen.get_width() // 2
    screenhalfy = screen.get_height() // 2
    iteration = 0
    chunks_for_visibility = 30
    chunk_size = (totalasteroids + chunks_for_visibility - 1) // chunks_for_visibility

    while running:
        deltatime = clock.get_time() * 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill(BLACK)

        pygame.draw.circle(screen, WHITE, (halfx, halfy) - ship.position, world_radius + 100, 100)
        ship.update(deltatime)

        shipx = ship.position.x
        shipy = ship.position.y
        drawnasteroids = 0

        start_index = (iteration % chunks_for_visibility) * chunk_size
        end_index = min(start_index + chunk_size, totalasteroids)
        for i in range(start_index, end_index):
            all_asteroids[i].check_visible(screenhalfx, screenhalfy, shipx, shipy)
        for asteroid in all_asteroids:
            if not asteroid.invisible:
                asteroid.update(screen, screenhalfx, screenhalfy, shipx, shipy, ship)
                drawnasteroids += 1

        iteration = (iteration + 1) % chunks_for_visibility

        # print("Drawn asteroids:", drawnasteroids)
        fps = clock.get_fps()
        osd.draw(ship, fps)
        ship.draw(screen)
        if ship.lives <= 0:
            running = False

        pygame.display.flip()
        clock.tick()

    pygame.quit()


if __name__ == "__main__":
    main()
