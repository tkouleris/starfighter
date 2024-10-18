from os import path
import pygame


class Bullet:
    def __init__(self, window):
        self.image = pygame.image.load(path.join('assets', '16x32_spaceship_shot_2.png'))
        self.visible = False
        self.bullet_velocity = 5
        self.x = 0
        self.y = 0
        self.window = window
        self.hitbox = pygame.Rect(self.x, self.y, 16, 32)

    def draw(self):
        if self.y <= 0:
            self.visible = False
        if self.visible:
            self.window.blit(self.image, (self.x, self.y))
            self.y -= self.bullet_velocity
        self.hitbox = pygame.Rect(self.x, self.y, 16, 32)

