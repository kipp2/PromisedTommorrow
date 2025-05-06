import pygame

class Floating_Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, color=(255, 255, 255), duration = 40):
        super().__init__()
        self.font = pygame.font.SysFont("arial", 18)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = duration 
        self.alive = True
        self.timer = 60  # lifespan in frames
        self.velocity = -1  # pixels to move upward per frame

    def update(self):
        self.rect.y += self.velocity
        self.timer -= 1
        if self.timer <= 0:
            self.alive = False 
