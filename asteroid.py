import pygame
import math
import random
from pygame.math import Vector2

class Asteroid:
    def __init__(self, x, y, radius):
        self.position = Vector2(x, y)
        self.radius = radius
        self.radiusextended = radius + 60
        self.radiussquared = radius**2
        # points around position creating asteroid.
        self.point = []
        for alpha in range(0, 360, 20):
            alpha_rad = math.radians(alpha)
            self.point.append(Vector2(self.radius * math.cos(alpha_rad), self.radius * math.sin(alpha_rad)) * random.uniform(0.8, 1.2))
        self.pointlength = len(self.point)
        # brown
        self.color = (150, 75, 0)
        self.invisible = True

    def check_visible(self, shipxleft, shipxright, shipytop, shipybottom):
        if (
            self.position.x  > shipxright
            or self.position.x < shipxleft
            or self.position.y > shipybottom
            or self.position.y < shipytop
            ):
            self.invisible = True
            return False
        self.invisible = False
        return True

    def update(self, screen, screenhalfx, screenhalfy, spaceshipx, spaceshipy, ship, clock):
        if self.invisible:
            return False

        self.draw(screen, screenhalfx, screenhalfy, spaceshipx, spaceshipy)

        distancesquar_to_spaceship_tip = Vector2.distance_squared_to(self.position, ship.tip)
        if distancesquar_to_spaceship_tip < self.radiussquared:
            ship.crash(clock)
            return True
        distancesquar_to_spaceship_left = Vector2.distance_squared_to(self.position, ship.left)
        if distancesquar_to_spaceship_left < self.radiussquared:
            ship.crash(clock)
            return True
        distancesquar_to_spaceship_right = Vector2.distance_squared_to(self.position, ship.right)
        if distancesquar_to_spaceship_right < self.radiussquared:
            ship.crash(clock)

        return True

    def draw(self, screen, screenhalfx, screenhalfy, spaceshipx, spaceshipy):
        # pygame.draw.circle(
        #     screen,
        #     BLUE,
        #     (
        #         int(self.position.x - spaceshipx + screenhalfx),
        #         int(self.position.y - spaceshipy + screenhalfy),
        #     ),
        #     int(self.radius),
        # )
        screenright=spaceshipx-screenhalfx
        screenbottom=spaceshipy-screenhalfy

        for point in range(1, self.pointlength):
            # pygame.draw.line(
            #     screen,
            #     WHITE,
            #     (
            #         int(self.position.x - spaceshipx + screenhalfx + self.point[point - 1].x),
            #         int(self.position.y - spaceshipy + screenhalfy + self.point[point - 1].y),
            #     ),
            #     (
            #         int(self.position.x - spaceshipx + screenhalfx + self.point[point].x),
            #         int(self.position.y - spaceshipy + screenhalfy + self.point[point].y),
            #     ),
            # )
            pygame.draw.polygon(
                screen,
                self.color,
                [
                    (
                        int(self.position.x - screenright + self.point[point - 1].x),
                        int(self.position.y - screenbottom + self.point[point - 1].y),
                    ),
                    (
                        int(self.position.x - screenright + self.point[point].x),
                        int(self.position.y - screenbottom  + self.point[point].y),
                    ),
                    (
                        int(self.position.x - screenright),
                        int(self.position.y - screenbottom),
                    ),
                ],
            )

        # pygame.draw.line(
        #     screen,
        #     WHITE,
        #     (
        #         int(self.position.x - spaceshipx + screenhalfx + self.point[0].x),
        #         int(self.position.y - spaceshipy + screenhalfy + self.point[0].y),
        #     ),
        #     (
        #         int(self.position.x - spaceshipx + screenhalfx + self.point[self.pointlength - 1].x),
        #         int(self.position.y - spaceshipy + screenhalfy + self.point[self.pointlength - 1].y),
        #     ),
        # )
        pygame.draw.polygon(
            screen,
            self.color,
            [
                (
                    int(self.position.x - screenright + self.point[0].x),
                    int(self.position.y - screenbottom + self.point[0].y),
                ),
                (
                    int(self.position.x - screenright + self.point[self.pointlength - 1].x),
                    int(self.position.y - screenbottom + self.point[self.pointlength - 1].y),
                ),
                (
                    int(self.position.x - screenright),
                    int(self.position.y - screenbottom),
                ),
            ],
        )
