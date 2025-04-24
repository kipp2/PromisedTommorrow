from config import WIDTH, HEIGHT, GREEN, GRAVITY
import pygame
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def generate_platforms():
    platforms = [Platform(200, HEIGHT-50, 400, 20)]
    for i in range(6):
        x = random.randint(100, WIDTH-200)
        y = HEIGHT - (i * 100) - 50 
        platforms.append(Platform(x, y, 200, 20))
    return platforms
