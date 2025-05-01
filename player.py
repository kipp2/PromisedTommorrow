import pygame
from config import GRAVITY, HEIGHT, BLUE, WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)  # Example starting position

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.score = 0
        self.swinging = False
        self.health = 3
        self.facing_right = True
        self.attack_cooldown = 0 
        self.swing_duration = 0
        self.hit_targets = set()

    def can_attack(self):
        return self.attack_cooldown == 0

    def update(self, platforms):
        self.vel_y += GRAVITY

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.attack_cooldown >0:
            self.attack_cooldown -= 1

        if self.swing_duration > 0:
            self.swing_duration -= 1
            if self.swing_duration == 0:
                self.swinging = False

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def move(self, direction):
        if direction == "left":
            self.vel_x = -5
            self.facing_right = False
        elif direction == "right":
            self.vel_x = 5
            self.facing_right = True

        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left >= WIDTH:
            self.rect.right = 0 

    def stop(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = -12
            self.on_ground = False
