import pygame
from config import RED 

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.image = pygame.Surface((40, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        if self.owner.swinging:
            self.image.set_alpha(255)
            if self.owner.facing_right:
                self.rect.midleft = (self.owner.rect.right, self.owner.rect.centery)
            else:
                self.rect.midright = (self.owner.rect.left, self.owner.rect.centery)
        else:
            self.image.set_alpha(0)