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
        self.state = "idle"
        self.attack_range = 40


    def update(self, platforms, player):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        self.platform = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.platform = platform
                elif self.vel_y == 0 and self.rect.bottom == platform.rect.top:
                    self.rect.x = max(platform.rect.left, min(self.rect.x, platform.rect.right - self.rect.width))
                    self.platform = platform
                break


        if self.platform:            
            if abs(player.rect.bottom - self.platform.rect.top) < 10 and \
           player.rect.right > self.platform.rect.left and \
           player.rect.left < self.platform.rect.right:
                distance = abs(self.rect.centerx - player.rect.centerx)
                if distance < self.attack_range:
                    self.state = "attack"
                elif distance < 200: 
                    self.state = "chase"
            else:
                self.state = "idle"

            if self.state == "chase":
                self.direction = 1 if self.rect.centerx < player.rect.centerx else -1
                self.rect.x += self.vel_x * self.direction
            elif self.state == "idle":
                self.rect.x += self.vel_x * self.direction
                if self.rect.left <= self.platform.rect.left or self.rect.right >= self.platform.rect.right:
                    self.direction *= -1
            elif self.state == "attack":
                pass
            print(f"Enemy State: {self.state} | X: {self.rect.x}")

        # Prevent falling below the screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
    
