from config import WIDTH, HEIGHT, RED, GRAVITY
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 3

        self.vel_x = 1
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1

    def update(self, platforms, player):
        self.vel_y += GRAVITY

        # Move horizontally
        self.rect.x += self.vel_x * self.direction

        # Reverse direction if hitting screen edges
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

        # Chase the player if within a certain distance
        distance = abs(self.rect.centerx - player.rect.centerx)
        if distance < 200:
            self.direction = 1 if self.rect.centerx < player.rect.centerx else -1

        # Move vertically
        self.rect.y += self.vel_y

        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # Prevent falling below the screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
