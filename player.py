from os import path
import pygame


class Player:

    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.image = pygame.image.load(path.join('assets', '32x32_spaceship.png'))
        self.height = 32
        self.width = 32
        self.visible = True
        self.hitbox = pygame.Rect(self.x, self.y, self.height, self.width)
        self.lives = 3

    def draw(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, self.height, self.width)
        self.window.blit(self.image, (self.x, self.y))


