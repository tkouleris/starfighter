import math
from os import path
import pygame
from enemy_bullet import EnemyBullet, aimed


class Boss:
    WIDTH = 96
    HEIGHT = 68
    # Where the boss stops after flying in from above the screen
    HOVER_Y = 40
    # Frames the boss stays highlighted after taking a hit
    FLASH_FRAMES = 4

    def __init__(self, window, number):
        # number is 1 for the first boss, 2 for the second, ...
        self.window = window
        self.visible = True
        self.image = pygame.transform.smoothscale(pygame.image.load(path.join('assets', 'enemy_1.png')),
                                                  (self.WIDTH, self.HEIGHT))
        self.flash_image = self.image.copy()
        self.flash_image.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_ADD)
        self.max_health = 25 + 15 * (number - 1)
        self.health = self.max_health
        self.speed = 1.5 + 0.25 * number
        self.bullet_speed = 3 + 0.25 * number
        self.x = (window.get_width() - self.WIDTH) / 2
        self.y = -self.HEIGHT
        self.direction = 1
        self.flash = 0
        self.attack_index = 0
        self.fire_timer = 60
        self.hitbox = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    @property
    def enraged(self):
        # Below half health the boss moves and fires faster
        return self.health <= self.max_health // 2

    def hit(self):
        # Returns True once the boss is destroyed
        self.health -= 1
        self.flash = self.FLASH_FRAMES
        if self.health <= 0:
            self.visible = False
        return not self.visible

    def move(self):
        if self.y < self.HOVER_Y:
            self.y += 1.5
            return
        speed = self.speed * (1.5 if self.enraged else 1)
        self.x += self.direction * speed
        max_x = self.window.get_width() - self.WIDTH
        if self.x <= 0 or self.x >= max_x:
            self.x = max(0, min(max_x, self.x))
            self.direction = -self.direction

    def fire(self, target):
        # Returns the bullets fired this frame (usually none), alternating between an aimed fan and a ring
        if self.y < self.HOVER_Y:
            return []
        self.fire_timer -= 1
        if self.fire_timer > 0:
            return []
        self.fire_timer = 50 if self.enraged else 80
        origin = (self.x + self.WIDTH / 2, self.y + self.HEIGHT - 10)
        self.attack_index += 1
        if self.attack_index % 2:
            count = 5 if self.enraged else 3
            return [aimed(self.window, origin, target, self.bullet_speed, (i - (count - 1) / 2) * 0.25)
                    for i in range(count)]
        count = 16 if self.enraged else 12
        # Rotate each ring by half a step so the gaps don't line up between rings
        offset = (self.attack_index // 2 % 2) * math.pi / count
        speed = self.bullet_speed * 0.75
        return [EnemyBullet(self.window, origin[0], origin[1],
                            math.cos(offset + i * 2 * math.pi / count) * speed,
                            math.sin(offset + i * 2 * math.pi / count) * speed)
                for i in range(count)]

    def draw(self):
        if self.visible:
            self.move()
            self.hitbox = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
            self.window.blit(self.flash_image if self.flash else self.image, (self.x, self.y))
            if self.flash:
                self.flash -= 1

    def draw_health_bar(self):
        if not self.visible:
            return
        width = 300
        x = (self.window.get_width() - width) // 2
        pygame.draw.rect(self.window, (60, 0, 0), (x, 12, width, 10))
        pygame.draw.rect(self.window, (255, 40, 40), (x, 12, width * self.health // self.max_health, 10))
        pygame.draw.rect(self.window, (255, 255, 255), (x, 12, width, 10), 1)
