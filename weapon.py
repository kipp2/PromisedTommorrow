import pygame
from config import RED 

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.image = pygame.Surface((40, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.original_image = self.image.copy()
        self.angle = 0 
        self.swinging = False

    def update(self):
        if self.owner.swinging:
            self.angle += 10 
            if self.angle > 90:
                self.angle = 0
                self.owner.swinging = False

            if self.owner.facing_right:
                pivot = (self.owner.rect.right, self.owner.rect.centery)
                offset = (20, 5)

            else:
                pivot = (self.owner.rect.left, self.owner.rect.centery)
                offset = (-20, -5)

            rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            self.image = rotated_image
            self.rect = self.image.get_rect()
            self.rect.topleft = (pivot[0] + offset[0], pivot[1] + offset[1])
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
            self.angle = 0 