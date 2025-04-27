import pygame
import random 
from enemy import Enemy

class Spawner:
    def __init__(self, platform):
        self.platforms = platform
        self.timer = 0
        self.activate = False

    def start(self):
        self.timer = pygame.time.get_ticks()
        self.activate = True

    def update(self, enemies):
        if self.activate:
            now = pygame.time.get_ticks()
            if now - self.timer > 5000:
                x = self.platform.rect.centerx - 20
                y = self.platform.rect.top - 60
                enemy = Enemy(x, y)
                enemy.platform = self.platform
                enemies.add(enemy)
                self.activate = False 