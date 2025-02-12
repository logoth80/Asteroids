import pygame
import pygame.font as font
from pygame import gfxdraw


class OSD:
    def __init__(self, screen):
        self.screen = screen
        self.font = font.SysFont(None, 36)
        self.text_color = (122, 122, 122)

    def draw(self, ship, fps):
        gfxdraw.filled_polygon(self.screen, [(10, 10), (310, 10), (310, 110), (10, 110)], (80, 80, 80, 85))
        pygame.draw.rect(self.screen, (90, 90, 90), (10, 10, 300, 100), 3, 5)

        text = f"Lives left: {ship.lives}"
        text_surface = self.font.render(text, True, self.text_color)
        self.screen.blit(text_surface, (15, 15))

        text = f"FPS: {fps:.0f}"
        text_surface = self.font.render(text, True, self.text_color)
        self.screen.blit(text_surface, (15, 45))
