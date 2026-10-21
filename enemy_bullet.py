import math
import pygame


class EnemyBullet:
    RADIUS = 5
    # Hitbox is smaller than the drawn shot so grazing it doesn't count as a hit
    HITBOX_SIZE = 6

    def __init__(self, window, x, y, dx, dy):
        self.window = window
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.visible = True
        self.hitbox = pygame.Rect(0, 0, self.HITBOX_SIZE, self.HITBOX_SIZE)
        self.hitbox.center = (self.x, self.y)

    def draw(self):
        self.x += self.dx
        self.y += self.dy
        if not (-self.RADIUS < self.x < self.window.get_width() + self.RADIUS and
                -self.RADIUS < self.y < self.window.get_height() + self.RADIUS):
            self.visible = False
        if self.visible:
            # Dark outline keeps the shot readable against the bright backgrounds
            pygame.draw.circle(self.window, (60, 0, 20), (self.x, self.y), self.RADIUS + 1)
            pygame.draw.circle(self.window, (255, 70, 40), (self.x, self.y), self.RADIUS)
            pygame.draw.circle(self.window, (255, 230, 160), (self.x, self.y), self.RADIUS // 2)
        self.hitbox.center = (self.x, self.y)


def aimed(window, origin, target, speed, angle_offset=0.0):
    # A bullet from origin towards target, optionally rotated by angle_offset radians
    angle = math.atan2(target[1] - origin[1], target[0] - origin[0]) + angle_offset
    return EnemyBullet(window, origin[0], origin[1], math.cos(angle) * speed, math.sin(angle) * speed)
