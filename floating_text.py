import pygame

class Floating_Text(pygame.sprite.Sprite):
    def __init__(self, text, pos, color=(255, 255, 255), lifetime = 60, dy=-1):
        super().__init__()
        self,font = pygame.font.SysFont(None, 24)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = lifetime
        self.dy = dy

    