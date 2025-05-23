import pygame
from pygame.locals import *
from enemy import Enemy  
from player import Player
from weapon import Weapon
from text import Text
from spawner import Spawner
from platforms import generate_platforms, Platform
from floating_text import Floating_Text
from config import WIDTH, HEIGHT, FPS, GRAVITY, WHITE, BLACK
import random

pygame.init()

SIZE = WIDTH, HEIGHT

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Promises Tommorrow")

player = Player()
floating_text = pygame.sprite.Group()
player.rect.bottomleft = (0, HEIGHT - 100)
weapon = Weapon(player)
platforms = generate_platforms()
score = 0 
font = pygame.font.SysFont(None, 36)

spawners = []
for plat in platforms:
    spawner = Spawner(plat)
    spawners.append(spawner)
    

def spawn_enemies_on_platforms():
    enemies = pygame.sprite.Group()
    for plat in platforms[1:]:
        enemy = Enemy(plat.rect.centerx - 20, plat.rect.top - 60)
        enemy.platform = plat
        enemies.add(enemy)
        for spawner in spawners:
            if spawner.platform == plat:
                spawner.current_enemy = enemy 
                break 
    return enemies

enemies = spawn_enemies_on_platforms()



clock = pygame.time.Clock()
running = True 
game_state = "menu"

while running:
    for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    if game_state == "menu":
        screen.fill(WHITE)
        title = Text("Promises Tomorrow", (WIDTH // 2, HEIGHT // 2 - 50), 50)
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

        if keys[pygame.K_z] and player.can_attack():
            player.swinging = True
            player.swing_duration = 10
            player.attack_cooldown = 30
            player.hit_targets.clear()
        

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
    
      
        for enemy in enemies:
            enemy.update(platforms, player)
            enemy.draw_health_bar(screen)
            enemy.draw(screen)
            if (
            weapon.rect.colliderect(enemy.rect) and player.swinging and enemy.state != "idle"
            ):
                direction = 1 if player.facing_right else -1
                old_health = enemy.health
                enemy.take_damage(direction)
                player.hit_targets.add(enemy)
                if enemy.health <= 0 and old_health > 0:                  
                    score += 10     
                
                    
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
