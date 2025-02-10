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
        target_angle = math.atan2(mouse_y - self.position.y, mouse_x - self.position.x)
        angle_diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi

        self.angle += angle_diff * self.turn_speed * deltatime

        self.direction = Vector2(math.cos(self.angle), math.sin(self.angle))

    def draw(self, screen):
        # Calculate the three points of the triangle
        x = self.position.x
        y = self.position.y
        angle = self.angle
        tip_x = int(x + math.cos(angle) * self.size)
        tip_y = int(y + math.sin(angle) * self.size)
        left_x = int(x + math.cos(angle + math.pi * 1.25) * self.size / 1.3)
        left_y = int(y + math.sin(angle + math.pi * 1.25) * self.size / 1.3)
        right_x = int(x + math.cos(angle - math.pi * 1.25) * self.size / 1.3)
        right_y = int(y + math.sin(angle - math.pi * 1.25) * self.size / 1.3)

        # Draw the triangle
        pygame.draw.polygon(screen, WHITE, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]], 1)
        print(self.speed, self.direction, self.angle)


def main():
    ship = Spaceship(640, 640)
    clock = pygame.time.Clock()

    running = True
    while running:
        deltatime = clock.get_time() * 0.1
        print("Deltatime:", deltatime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill(BLACK)
        ship.update(deltatime)
        ship.draw(screen)
        pygame.display.flip()
        clock.tick(144)


if __name__ == "__main__":
    main()
