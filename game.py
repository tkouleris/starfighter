from os import path
import pygame
import random
from bullet import Bullet
from collision import Collision
from enemy import Enemy
from enemy_animations import line, zig_zag, circle
from explosion import Explosion
from player import Player
from power_up import PowerUp
from weapons import BLASTER, POWER_UPS


class Game:
    POWER_UP_CHANCE = 0.15
    # How long a power-up weapon lasts, in frames
    POWER_UP_DURATION = 600

    def __init__(self, level, settings):
        self.level = level
        self.settings = settings
        self.score = 0
        self.paused = None
        self.spaceship_x = None
        self.spaceship_y = None
        self.init_spaceship_y = None
        self.init_spaceship_x = None
        self.enemies = []
        self.explosions = []
        self.bullets = []
        self.power_ups = []
        self.weapon = BLASTER
        self.weapon_timer = 0
        self.fire_cooldown = 0
        self.window_width = 640
        self.window_height = 480
        self.win = pygame.display.set_mode((self.window_width, self.window_height))
        self.bg = [pygame.image.load(path.join('assets', '1.jpg')), pygame.image.load(path.join('assets', '2.jpg')),
                   pygame.image.load(path.join('assets', '3.jpg'))]
        self.bg_x = 0
        self.bg_y = 0
        self.bullet_sound = pygame.mixer.Sound(path.join('assets', 'sounds', 'bullet.mp3'))
        self.explosion = pygame.mixer.Sound(path.join('assets', 'sounds', 'explosion.mp3'))
        settings.register_sound(self.bullet_sound)
        settings.register_sound(self.explosion)
        self.collision = Collision()
        self.font = pygame.font.SysFont('comicsans', 20, True, True)
        pygame.display.set_caption("Star Fighter")
        self.bullet_image = pygame.image.load(path.join('assets', '16x32_spaceship_shot_2.png'))
        self.enemy_movement = [line, zig_zag]
        self.player = Player(self.win, (self.window_width // 2) - (32 // 2), self.window_height - 32 - 5)
        self.init_game()

    def init_game(self):
        self.enemies = []
        self.explosions = []
        self.bullets = []
        self.power_ups = []
        self.fire_cooldown = 0
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
            if self.fire_cooldown > 0:
                self.fire_cooldown -= 1
            if self.weapon_timer > 0:
                self.weapon_timer -= 1
                if self.weapon_timer == 0:
                    self.weapon = BLASTER

            # Controls are dead while the player's ship is exploding
            if self.player.visible:
                keys = pygame.key.get_pressed()
                controls = self.settings.controls
                if keys[controls['right']] and self.spaceship_x < (self.window_width - 32):
                    self.spaceship_x += 2
                if keys[controls['left']] and self.spaceship_x > 0:
                    self.spaceship_x -= 2
                if keys[controls['up']]:
                    self.spaceship_y -= 2
                if keys[controls['down']] and (self.spaceship_y + 32) < self.window_height:
                    self.spaceship_y += 2
                if keys[controls['fire']] and self.fire_cooldown == 0:
                    self.bullet_sound.play()
                    self.fire_cooldown = self.weapon.cooldown
                    for offset, dx in self.weapon.shots:
                        # Bullets are 16 wide, so +8 centres them on the 32-wide ship
                        self.bullets.append(Bullet(self.win, self.bullet_image, self.spaceship_x + 8 + offset,
                                                   self.spaceship_y - 35, dx))

            self.win.blit(self.bg[self.level % 3], (self.bg_x, self.bg_y))

            for bullet in self.bullets:
                bullet.draw()
            if self.player.visible:
                self.player.draw(self.spaceship_x, self.spaceship_y)
            for enemy in self.enemies:
                enemy.draw()
                if enemy.y >= self.window_height:
                    x = random.randint(32, 448)
                    enemy.set_init(x, 0, self.enemy_movement[random.randint(0, 1)])
                for bullet in self.bullets:
                    if self.collision.check(enemy, bullet, self.explosion):
                        self.score += 10 * self.level
                        self.explosions.append(Explosion(self.win, enemy.hitbox.center))
                        if random.random() < self.POWER_UP_CHANCE:
                            self.power_ups.append(
                                PowerUp(self.win, random.choice(POWER_UPS), enemy.hitbox.center, self.font))
                if self.collision.check(enemy, self.player, self.explosion):
                    self.explosions.append(Explosion(self.win, self.player.hitbox.center, 1.6, 50))

            self.bullets = [bullet for bullet in self.bullets if bullet.visible]

            for power_up in self.power_ups:
                power_up.draw()
                # Not Collision.check: catching a power-up must not hide the player
                if self.player.visible and power_up.visible and power_up.hitbox.colliderect(self.player.hitbox):
                    power_up.visible = False
                    self.weapon = power_up.weapon
                    self.weapon_timer = self.POWER_UP_DURATION
            self.power_ups = [power_up for power_up in self.power_ups if power_up.visible]

            for explosion in self.explosions:
                explosion.draw()
            self.explosions = [explosion for explosion in self.explosions if not explosion.finished]

            # A hit player stays invisible until its explosion has played out, then the round ends
            if not self.player.visible and not self.explosions:
                self.player.visible = True
                self.spaceship_x = self.init_spaceship_x
                self.spaceship_y = self.init_spaceship_y
                self.paused = True
                self.player.lives -= 1
                self.weapon = BLASTER
                self.weapon_timer = 0

            text = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
            self.win.blit(text, (10, 10))
            if self.weapon_timer > 0:
                text = self.font.render(f"{self.weapon.name}: {self.weapon_timer // 60 + 1}s", 1, self.weapon.color)
                self.win.blit(text, (10, 35))
