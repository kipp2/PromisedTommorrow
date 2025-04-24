import pygame
from config import BLACK

class Text:
    def __init__(self, text, pos, font_size=36, color=BLACK, font=None):
        self.text = text
        self.pos = pos
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.render()

    def render(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_text(self, new_text):
        self.text = new_text
        self.render()
