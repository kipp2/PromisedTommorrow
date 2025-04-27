from config import WIDTH, HEIGHT, RED, GRAVITY, GREEN, BLACK
import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100

        self.vel_x = 1
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1
        self.state = "idle"
        self.attack_range = 40
        self.knockback_timer = 0 
        self.knockback_force = 8 


    def update(self, platforms, player):
        # 1) Gravity & vertical movement
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # 2) Knockback movement (if active)
        if self.knockback_timer > 0:
            self.rect.x += self.knockback_force * self.direction
            self.knockback_timer -= 1
            # clamp to platform edges if still on one
            if self.platform:
                self.rect.left = max(self.rect.left, self.platform.rect.left)
                self.rect.right = min(self.rect.right, self.platform.rect.right)

        # 3) Detect “real” platforms
        self.platform = None
        self.on_ground = False
        for plat in platforms:
            if (self.rect.centerx > plat.rect.left + 5 and
                self.rect.centerx < plat.rect.right - 5 and
                abs(self.rect.bottom - plat.rect.top) < 10 and
                self.vel_y >= 0):
                # Snap to that platform
                self.rect.bottom = plat.rect.top
                self.vel_y = 0
                self.platform = plat
                self.on_ground = True
                break

        # 4) If no platform, snap to floor
        if not self.platform:
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.vel_y = 0
                self.on_ground = True
                self.on_floor = True
            else:
                self.on_floor = False

        # 5) AI & movement
        if self.platform or self.on_floor:
            # determine if player is “on the same surface”
            on_same_surface = False
            if self.platform:
                on_same_surface = (
                    abs(player.rect.bottom - self.platform.rect.top) < 10 and
                    player.rect.centerx > self.platform.rect.left and
                    player.rect.centerx < self.platform.rect.right
                )
            else:
                on_same_surface = self.on_floor

            # distance check
            dist = abs(self.rect.centerx - player.rect.centerx)
            if on_same_surface:
                if dist < self.attack_range:
                    self.state = "attack"
                elif dist < 200:
                    self.state = "chase"
                else:
                    self.state = "idle"
            else:
                self.state = "idle"

            # perform movement per state
            if self.state == "chase":
                self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
            if self.state in ("chase", "idle"):
                self.rect.x += self.vel_x * self.direction

            # reverse at edges
            left_bound = self.platform.rect.left if self.platform else 0
            right_bound = self.platform.rect.right if self.platform else WIDTH
            if self.rect.left <= left_bound or self.rect.right >= right_bound:
                self.direction *= -1

            # final clamp to keep them “on” the platform/floor
            if self.platform:
                self.rect.left = max(self.rect.left, left_bound)
                self.rect.right = min(self.rect.right, right_bound)
            else:
                # floor: world edges
                self.rect.left = max(self.rect.left, 0)
                self.rect.right = min(self.rect.right, WIDTH)

        # 6) If still airborne (no platform & not yet reached floor), do nothing until landing

        # (Optional debug)
        # print(f"[Enemy] State={self.state}  Plat={self.platform}  Floor={self.on_floor}  X={self.rect.x}")

        
        

    #take damage
    def take_damage(self, attacker_direction):
        damage = random.randint(0, 12)
        if damage == 0:
            print("Miss")
            return 
        elif damage >= 10:
            print("Critical Hit")
            self.health -= damage 
        else:
            print(f"Hit! Damage: {damage}")
            self.health -= damage
        
        self.vel_y = -5
        self.knockback_timer = 10
        self.direction = attacker_direction
        if self.health <= 0:
            print("Kill") 
            self.kill()
    
    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 5
        fill = (self.health /100) * bar_width
        #outline_rect = pygame.Rect(self.rect.x, self.rect.y - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 10 , fill, bar_height)
        pygame.draw.rect(surface, GREEN, fill_rect)
        #pygame.draw.rect(surface, BLACK, outline_rect)