import pygame
import random 
from enemy import Enemy

class Spawner:
    def __init__(self, platform):
        self.platform = platform
        self.timer = 0
        self.activate = False
        self.current_enemy = None

    def update(self, enemies):

        if self.current_enemy and not self.current_enemy.alive():
            self.current_enemy = None
            self.start()

        if self.activate:
            now = pygame.time.get_ticks()
            print(f"Spawner activate! Time; {now} - Timer start: {self.timer}")
            if now - self.timer > 2000:
                x = self.platform.rect.centerx - 20
                y = self.platform.rect.top - 60
                enemy = Enemy(x, y)
                enemy.platform = self.platform
                enemies.add(enemy)
                self.current_enemy = enemy 
                self.activate = False 

    def start(self):
        self.timer = pygame.time.get_ticks()
        self.activate = True