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
    for i in range(6000):
        radius = world_radius * math.sqrt(random.random())
        alpha = random.uniform(0, 2 * math.pi)
        x = radius * math.cos(alpha)
        y = radius * math.sin(alpha)
        one_asteroid = Asteroid(x, y, random.randint(20, 50))
        all_asteroids.append(one_asteroid)

    clock = pygame.time.Clock()
    osd = OSD(screen)

    global running
    screenhalfx = screen.get_width() // 2
    screenhalfy = screen.get_height() // 2
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
        for asteroid in all_asteroids:
            if asteroid.update(screen, screenhalfx, screenhalfy, shipx, shipy, ship):
                drawnasteroids += 1
        # print("Drawn asteroids:", drawnasteroids)
        osd.draw(ship)
        ship.draw(screen)
        if ship.lives <= 0:
            running = False

        pygame.display.flip()
        clock.tick()
        if pygame.time.get_ticks() % 100 == 0:
            # print(f"position: {ship.position}, tip: {ship.tip}")
            print(f"fps: {clock.get_fps()}")


if __name__ == "__main__":
    main()
