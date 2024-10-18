from os import path
import pygame
import random
from bullet import Bullet
from collision import Collision
from enemy import Enemy
from enemy_animations import line, zig_zag, circle
from player import Player


class Game:
    def __init__(self, level):
        self.level = level
        self.paused = None
        self.spaceship_x = None
        self.spaceship_y = None
        self.init_spaceship_y = None
        self.init_spaceship_x = None
        self.enemies = []
        self.window_width = 640
        self.window_height = 480
        self.win = pygame.display.set_mode((self.window_width, self.window_height))
        self.bg = [pygame.image.load(path.join('assets', '1.jpg')), pygame.image.load(path.join('assets', '2.jpg')),
                   pygame.image.load(path.join('assets', '3.jpg'))]
        self.bg_x = 0
        self.bg_y = 0
        self.bullet_sound = pygame.mixer.Sound(path.join('assets', 'sounds', 'bullet.mp3'))
        self.explosion = pygame.mixer.Sound(path.join('assets', 'sounds', 'explosion.mp3'))
        self.collision = Collision()
        pygame.display.set_caption("Star Fighter")
        self.bullet = Bullet(self.win)
        self.enemy_movement = [line, zig_zag]
        self.player = Player(self.win, (self.window_width // 2) - (32 // 2), self.window_height - 32 - 5)
        self.init_game()

    def init_game(self):
        self.enemies = []
        for index in range(self.level):
            self.enemies.append(
                Enemy(self.win, 100, 100, self.enemy_movement[random.randint(0, 1)], random.randint(3, 5)))

        self.init_spaceship_x = (self.window_width // 2) - (32 // 2)
        self.init_spaceship_y = self.window_height - 32 - 5
        self.spaceship_x = (self.window_width // 2) - (32 // 2)
        self.spaceship_y = self.window_height - 32 - 5

        self.paused = False

    def handle(self):
        if not self.paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.spaceship_x < (self.window_width - 32):
                self.spaceship_x += 2
            if keys[pygame.K_LEFT] and self.spaceship_x > 0:
                self.spaceship_x -= 2
            if keys[pygame.K_UP]:
                self.spaceship_y -= 2
            if keys[pygame.K_DOWN] and (self.spaceship_y + 32) < self.window_height:
                self.spaceship_y += 2
            if keys[pygame.K_SPACE] and not self.bullet.visible:
                self.bullet_sound.play()
                self.bullet.visible = True
                self.bullet.x = self.spaceship_x
                self.bullet.y = self.spaceship_y - 35

            self.win.blit(self.bg[self.level % 3], (self.bg_x, self.bg_y))

            self.bullet.draw()
            self.player.draw(self.spaceship_x, self.spaceship_y)
            for enemy in self.enemies:
                enemy.draw()
                if enemy.y >= self.window_height:
                    x = random.randint(32, 448)
                    enemy.set_init(x, 0, self.enemy_movement[random.randint(0, 1)])
                self.collision.check(enemy, self.bullet, self.explosion)
                self.collision.check(enemy, self.player)
                if not self.player.visible:
                    self.player.visible = True
                    self.spaceship_x = self.init_spaceship_x
                    self.spaceship_y = self.init_spaceship_y
                    self.paused = True
                    self.player.lives -= 1
