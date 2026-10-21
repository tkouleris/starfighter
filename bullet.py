import pygame


class Bullet:
    def __init__(self, window, image, x, y, dx=0):
        self.image = image
        self.visible = True
        self.bullet_velocity = 5
        self.x = x
        self.y = y
        self.dx = dx
        self.window = window
        self.hitbox = pygame.Rect(self.x, self.y, 16, 32)

    def draw(self):
        if self.y <= -32 or not -16 < self.x < self.window.get_width():
            self.visible = False
        if self.visible:
            self.window.blit(self.image, (self.x, self.y))
            self.y -= self.bullet_velocity
            self.x += self.dx
        self.hitbox = pygame.Rect(self.x, self.y, 16, 32)
