from os import path
import pygame
import random


class Enemy:
    def __init__(self, window, x, y, animation, velocity=3):
        self.window = window
        self.visible = True
        self.x = x
        self.y = y
        self.image = pygame.image.load(path.join('assets', '32x32_enemy_1.png'))
        self.height = 32
        self.width = 32
        self.direction = 1
        self.velocity = velocity
        self.animation = animation
        self.move_index = 0
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def move(self):
        self.animation(self)

    def set_init(self, x, y, animation):
        self.x = x
        self.y = y
        self.animation = animation

    def draw(self):
        if self.visible:
            self.move()
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)
            self.window.blit(self.image, (self.x, self.y))
