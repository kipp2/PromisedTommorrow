import pygame
from pygame.locals import *
from enemy import Enemy  # Import the Enemy class
from player import Player
from weapon import Weapon
from text import Text
from spawner import Spawner
from platforms import generate_platforms, Platform
from config import WIDTH, HEIGHT, FPS, GRAVITY, WHITE, BLACK
import random

pygame.init()

SIZE = WIDTH, HEIGHT

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PromisedTommorrow")

player = Player()
player.rect.bottomleft = (0, HEIGHT - 100)
weapon = Weapon(player)
platforms = generate_platforms()
score = 0 
font = pygame.font.SysFont(None, 36)

# Create an enemy instance
def spawn_enemies_on_platforms():
    enemies = pygame.sprite.Group()
    for plat in platforms[1:]:
        enemy = Enemy(plat.rect.centerx - 20, plat.rect.top - 60)
        enemy.platform = plat
        enemies.add(enemy)
    return enemies

enemies = spawn_enemies_on_platforms()

spawners = []
clock = pygame.time.Clock()
running = True 
game_state = "menu"

while running:
    for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    if game_state == "menu":
        screen.fill(WHITE)
        title = Text("Promised Tomorrow", (WIDTH // 2, HEIGHT // 2 - 50), 50)
        start = Text("Press Enter to Start", (WIDTH // 2, HEIGHT // 2), 50)
        title.draw(screen)
        start.draw(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = "game"

    elif game_state == "game":
        screen.fill(WHITE)

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
        weapon.update()
        score_text = font.render(f"Score: {score}", True, BLACK)

    # Draw player and enemy
        screen.blit(player.image, player.rect)
        screen.blit(weapon.image, weapon.rect)
        screen.blit(score_text, (10, 10))

    # Update platforms
        platforms = [p for p in platforms if p.rect.top < HEIGHT]

        if len(platforms) < 6:
            x = random.randint(100, WIDTH - 200)
            y = platforms[-1].rect.top - 100
            platforms.append(Platform(x, y, 200, 20))

        for spawner in spawners:
            spawner.update(enemies)

        for platform in platforms:
            screen.blit(platform.image, platform.rect)
    
        enemies.update(platforms, player)
        for enemy in enemies:
            enemy.draw_health_bar(screen)
            screen.blit(enemy.image, enemy.rect)
            if (
            weapon.rect.colliderect(enemy.rect) and player.swinging and enemy.state != "idle"
            ):
                direction = 1 if player.facing_right else -1
                old_health = enemy.health
                enemy.take_damage(direction)
                if enemy.health <= 0 and old_health > 0: 
                    score += 10 
                    spawner = Spawner(enemy.platform)
                    spawner.start()
                    spawners.append(spawner)
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
