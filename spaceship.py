import pygame
import math
from pygame.math import Vector2


# Spaceship class
class Spaceship:
    def __init__(self, x, y):
        self.color = (255, 255, 255)
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
        self.deltapos += self.direction * self.acceleration * deltatime
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
        halfx = screen.get_width() / 2
        halfy = screen.get_height() / 2
        dx = self.position.x - halfx
        dy = self.position.y - halfy
        self.tip = Vector2(tip_x + dx, tip_y + dy)
        self.left = Vector2(left_x + dx, left_y + dy)
        self.right = Vector2(right_x + dx, right_y + dy)

        # Draw the triangle
        if self.invulnerable:
            pygame.draw.polygon(screen, self.color, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]])
        else:
            pygame.draw.polygon(screen, self.color, [[tip_x, tip_y], [left_x, left_y], [right_x, right_y]], 1)
