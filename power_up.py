import pygame


class PowerUp:
    RADIUS = 12

    def __init__(self, window, weapon, center, font):
        self.window = window
        self.weapon = weapon
        self.x, self.y = center
        self.font = font
        self.velocity = 2
        self.visible = True
        self.hitbox = pygame.Rect(self.x - self.RADIUS, self.y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)

    def draw(self):
        self.y += self.velocity
        if self.y - self.RADIUS > self.window.get_height():
            self.visible = False
        if self.visible:
            pygame.draw.circle(self.window, self.weapon.color, (self.x, self.y), self.RADIUS)
            pygame.draw.circle(self.window, (255, 255, 255), (self.x, self.y), self.RADIUS, 2)
            text = self.font.render(self.weapon.name[0], 1, (255, 255, 255))
            self.window.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))
        self.hitbox = pygame.Rect(self.x - self.RADIUS, self.y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)
