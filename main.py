import pygame
from pygame.math import Vector2
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1280
halfx = SCREEN_WIDTH // 2
halfy = SCREEN_HEIGHT // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game")
world_radius = 5000
running = True


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
        self.radiussquared = radius**2

    def update(self, screenhalfx, screenhalfy, spaceshipx, spaceshipy, ship):
        if (
            self.position.x - self.radius > spaceshipx + screenhalfx
            or self.position.x + self.radius < spaceshipx - screenhalfx
            or self.position.y - self.radius > spaceshipy + screenhalfy
            or self.position.y + self.radius < spaceshipy - screenhalfx
        ):
            return False
        self.draw(screenhalfx, screenhalfy, spaceshipx, spaceshipy)

        distancesquar_to_spaceship_tip = Vector2.distance_squared_to(self.position, ship.tip)
        if distancesquar_to_spaceship_tip < self.radiussquared:
            ship.crash(ship.tip)
        distancesquar_to_spaceship_left = Vector2.distance_squared_to(self.position, ship.left)
        if distancesquar_to_spaceship_left < self.radiussquared:
            ship.crash(ship.left)
        distancesquar_to_spaceship_right = Vector2.distance_squared_to(self.position, ship.right)
        if distancesquar_to_spaceship_right < self.radiussquared:
            ship.crash(ship.right)

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
        self.deltapos = Vector2(0, 0)
        self.turn_speed = 0.1
        self.size = 30
        self.maxspeed = 3
        self.acceleration = 0.1
        self.lives = 3
        self.tip = Vector2(int(x + math.cos(self.angle) * self.size), int(y + math.sin(self.angle) * self.size))
        self.left = Vector2(
            int(x + math.cos(self.angle + math.pi * 1.25) * self.size / 1.3), int(y + math.sin(self.angle + math.pi * 1.25) * self.size / 1.3)
        )
        self.right = Vector2(
            int(x + math.cos(self.angle - math.pi * 1.25) * self.size / 1.3), int(y + math.sin(self.angle - math.pi * 1.25) * self.size / 1.3)
        )
        self.invulnerable = True
        self.invulnerable_duration = 1500
        self.activate_at = pygame.time.get_ticks() + self.invulnerable_duration

    def update(self, deltatime):
        self.deltapos += self.direction * self.acceleration
        self.deltapos = self.deltapos.clamp_magnitude(self.maxspeed)
        self.position += self.deltapos * deltatime
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_angle = math.atan2(mouse_y - 640, mouse_x - 640)
        angle_diff = (target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        self.angle += angle_diff * self.turn_speed * deltatime
        self.direction = Vector2(math.cos(self.angle), math.sin(self.angle))
        if self.invulnerable:
            if self.activate_at <= pygame.time.get_ticks():
                self.invulnerable = False

    def crash(self, collisionpos):
        if self.invulnerable:
            if self.activate_at <= pygame.time.get_ticks():
                self.invulnerable = False
        else:
            self.invulnerable = True
            self.activate_at = pygame.time.get_ticks() + self.invulnerable_duration
            self.lives -= 1
            print(f"Crash! Lives: {self.lives}")

            if self.lives <= 0:
                global running
                running = False

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
        dx = self.position.x - halfx
        dy = self.position.y - halfy
        self.tip = Vector2(tip_x + dx, tip_y + dy)
        self.left = Vector2(left_x + dx, left_y + dy)
        self.right = Vector2(right_x + dx, right_y + dy)

        # Draw the triangle
        if self.invulnerable:
            pygame.draw.polygon(screen, WHITE, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]])
        else:
            pygame.draw.polygon(screen, WHITE, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]], 1)


def main():
    ship = Spaceship(0, 0)
    all_asteroids = []
    for i in range(1000):
        radius = world_radius * math.sqrt(random.random())
        alpha = random.uniform(0, 2 * math.pi)
        x = radius * math.cos(alpha)
        y = radius * math.sin(alpha)
        asteroid = Asteroid(x, y, random.randint(20, 50))
        all_asteroids.append(asteroid)

    clock = pygame.time.Clock()
    global running
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

        screenhalfx = screen.get_width() / 2
        screenhalfy = screen.get_height() / 2
        shipx = ship.position.x
        shipy = ship.position.y
        drawnasteroids = 0
        for asteroid in all_asteroids:
            if asteroid.update(screenhalfx, screenhalfy, shipx, shipy, ship):
                drawnasteroids += 1
        # print("Drawn asteroids:", drawnasteroids)

        ship.draw(screen)
        pygame.display.flip()
        clock.tick()
        if pygame.time.get_ticks() % 1000 == 0:
            print(f"position: {ship.position}, tip: {ship.tip}")


if __name__ == "__main__":
    main()
