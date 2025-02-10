import pygame
from pygame.math import Vector2
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1280
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Asteroid:
    def __init__(self, x, y, radius):
        self.position = Vector2(x, y)
        self.radius = radius

    def update(self, screenhalfx, screenhalfy, spaceshipx, spaceshipy):
        if (
            self.position.x - self.radius > spaceshipx + screenhalfx
            or self.position.x + self.radius < spaceshipx - screenhalfx
            or self.position.y - self.radius > spaceshipy + screenhalfy
            or self.position.y + self.radius < spaceshipy - screenhalfx
        ):
            return False
        self.draw(screenhalfx, screenhalfy, spaceshipx, spaceshipy)
        return True

    def draw(self, screenhalfx, screenhalfy, spaceshipx, spaceshipy):
        pygame.draw.circle(
            screen,
            WHITE,
            (
                int(self.position.x - spaceshipx + screenhalfx),
                int(self.position.y - spaceshipy + screenhalfy),
            ),
            int(self.radius),
        )


# Spaceship class
class Spaceship:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.direction = Vector2(0, 1)
        self.angle = 0
        self.speed = Vector2(0, 0)
        self.turn_speed = 0.1
        self.size = 30
        self.maxspeed = 3
        self.acceleration = 0.1

    def update(self, deltatime):
        self.speed += self.direction * self.acceleration
        self.speed = self.speed.clamp_magnitude(self.maxspeed)
        self.position += self.speed * deltatime
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_angle = math.atan2(mouse_y - 640, mouse_x - 640)
        angle_diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

        self.angle += angle_diff * self.turn_speed * deltatime

        self.direction = Vector2(math.cos(self.angle), math.sin(self.angle))

    def draw(self, screen):
        # Calculate the three points of the triangle
        x = 640
        y = 640

        angle = self.angle
        tip_x = int(x + math.cos(angle) * self.size)
        tip_y = int(y + math.sin(angle) * self.size)
        left_x = int(x + math.cos(angle + math.pi * 1.25) * self.size / 1.3)
        left_y = int(y + math.sin(angle + math.pi * 1.25) * self.size / 1.3)
        right_x = int(x + math.cos(angle - math.pi * 1.25) * self.size / 1.3)
        right_y = int(y + math.sin(angle - math.pi * 1.25) * self.size / 1.3)

        # Draw the triangle
        pygame.draw.polygon(screen, WHITE, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]], 1)


def main():
    ship = Spaceship(640, 640)
    all_asteroids = []
    for i in range(100):
        asteroid = Asteroid(random.randint(-5000, 5000), random.randint(-5000, 5000), random.randint(20, 50))
        all_asteroids.append(asteroid)

    clock = pygame.time.Clock()

    running = True
    while running:
        deltatime = clock.get_time() * 0.1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill(BLACK)
        ship.update(deltatime)

        screenhalfx = screen.get_width() / 2
        screenhalfy = screen.get_height() / 2
        shipx = ship.position.x
        shipy = ship.position.y
        drawnasteroids = 0
        for asteroid in all_asteroids:
            if asteroid.update(screenhalfx, screenhalfy, shipx, shipy):
                drawnasteroids += 1
        print("Drawn asteroids:", drawnasteroids)

        ship.draw(screen)
        pygame.display.flip()
        clock.tick(144)


if __name__ == "__main__":
    main()
