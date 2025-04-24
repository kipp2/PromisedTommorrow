import pygame
from pygame.locals import *
from enemy import Enemy  # Import the Enemy class
from player import Player
from weapon import Weapon
from platforms import generate_platforms, Platform
from config import WIDTH, HEIGHT, FPS, GRAVITY, WHITE
import random

pygame.init()

SIZE = WIDTH, HEIGHT

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PromisedTommorrow")

player = Player()
weapon = Weapon(player)
platforms = generate_platforms()

# Create an enemy instance
enemies = pygame.sprite.Group()
enemy = Enemy(300, HEIGHT - 120)  # Example starting position for the enemy
enemies.add(enemy)

clock = pygame.time.Clock()
running = True 

while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    elif keys[pygame.K_RIGHT]:
        player.move("right")
    else:
        player.stop()

    if keys[pygame.K_SPACE]:
        player.jump()

    if keys[pygame.K_z]:
        player.swinging = True
        
    else:
        player.swinging = False
        

    # Update player and enemy
    player.update(platforms)
    enemy.update(platforms, player)  # Pass platforms and player to the enemy's update method
    weapon.update()

    # Draw player and enemy
    screen.blit(player.image, player.rect)
    screen.blit(weapon.image, weapon.rect)
    # Update platforms
    platforms = [p for p in platforms if p.rect.top < HEIGHT]

    if len(platforms) < 6:
        x = random.randint(100, WIDTH - 200)
        y = platforms[-1].rect.top - 100
        platforms.append(Platform(x, y, 200, 20))

    for platform in platforms:
        screen.blit(platform.image, platform.rect)
    
    enemies.update(platforms, player)
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)
        if weapon.rect.colliderect(enemy.rect):
            enemy.take_damage()
    pygame.display.update()
pygame.quit()
