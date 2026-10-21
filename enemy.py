from os import path
import pygame
import random


class Enemy:
    # Frames between shots, picked at random from this range
    FIRE_INTERVAL = (90, 240)

    def __init__(self, window, x, y, animation, velocity=3):
        self.window = window
        self.visible = True
        self.image = pygame.image.load(path.join('assets', '32x32_enemy_1.png'))
        self.height = 32
        self.width = 32
        self.velocity = velocity
        self.set_init(x, y, animation)
        self.hitbox = pygame.Rect(self.x, self.y, 32, 32)

    def move(self):
        self.animation(self)

    def set_init(self, x, y, animation):
        self.x = x
        self.y = y
        self.animation = animation
        # Per-pattern state, reset so a respawned enemy starts its new pattern cleanly
        self.direction = random.choice((-1, 1))
        self.move_index = 0
        self.anchor_x = x
        self.anchor_y = y
        self.fire_timer = random.randint(*self.FIRE_INTERVAL)

    def ready_to_fire(self):
        # Only fire from the top half of the screen, so shots are never point-blank
        if not self.visible or not 0 <= self.y <= self.window.get_height() // 2:
            return False
        self.fire_timer -= 1
        if self.fire_timer > 0:
            return False
        self.fire_timer = random.randint(*self.FIRE_INTERVAL)
        return True

    def draw(self):
        if self.visible:
            self.move()
            self.hitbox = pygame.Rect(self.x, self.y, 32, 32)
            self.window.blit(self.image, (self.x, self.y))
