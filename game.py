from os import path
import pygame
import random
from boss import Boss
from bullet import Bullet
from collision import Collision
from enemy import Enemy
from enemy_animations import line, zig_zag, circle
from enemy_bullet import aimed
from explosion import Explosion
from player import Player
from power_up import PowerUp
from weapons import BLASTER, POWER_UPS


class Game:
    POWER_UP_CHANCE = 0.15
    # How long a power-up weapon lasts, in frames
    POWER_UP_DURATION = 600
    # Ship movement: top speed in pixels per frame, and how quickly velocity eases towards
    # the held direction (higher = snappier, 1 = instant start/stop)
    SHIP_SPEED = 4.5
    SHIP_RESPONSIVENESS = 0.25
    # Every Nth level is a boss fight instead of a wave of enemies
    BOSS_LEVEL_INTERVAL = 5
    ENEMY_BULLET_SPEED = 3
    # Vertical gap between enemies flying in at the start of a level, picked at random per enemy
    SPAWN_GAP = (40, 100)

    def __init__(self, level, settings):
        self.level = level
        self.settings = settings
        self.score = 0
        self.paused = None
        self.spaceship_x = None
        self.spaceship_y = None
        self.velocity_x = 0
        self.velocity_y = 0
        self.init_spaceship_y = None
        self.init_spaceship_x = None
        self.enemies = []
        self.boss = None
        self.explosions = []
        self.bullets = []
        self.enemy_bullets = []
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
        self.enemy_movement = [line, zig_zag, circle]
        self.player = Player(self.win, (self.window_width // 2) - (32 // 2), self.window_height - 32 - 5)
        self.init_game()

    def is_boss_level(self):
        return self.level % self.BOSS_LEVEL_INTERVAL == 0

    def level_cleared(self):
        return not any(enemy.visible for enemy in self.enemies) and not (self.boss and self.boss.visible)

    def init_game(self):
        self.enemies = []
        self.boss = None
        self.explosions = []
        self.bullets = []
        self.enemy_bullets = []
        self.power_ups = []
        self.fire_cooldown = 0
        if self.is_boss_level():
            self.boss = Boss(self.win, self.level // self.BOSS_LEVEL_INTERVAL)
        else:
            # Spread enemies across the width and stagger them above the screen so they fly in one by one
            x = None
            y = -32
            for _ in range(self.level):
                x = self.random_spawn_x(x)
                self.enemies.append(
                    Enemy(self.win, x, y, random.choice(self.enemy_movement), random.randint(3, 5)))
                y -= random.randint(*self.SPAWN_GAP)

        self.init_spaceship_x = (self.window_width // 2) - (32 // 2)
        self.init_spaceship_y = self.window_height - 32 - 5
        self.spaceship_x = (self.window_width // 2) - (32 // 2)
        self.spaceship_y = self.window_height - 32 - 5
        self.velocity_x = 0
        self.velocity_y = 0

        self.paused = False

    def move_spaceship(self, direction_x, direction_y):
        target_x = direction_x * self.SHIP_SPEED
        target_y = direction_y * self.SHIP_SPEED
        # Diagonals would otherwise be ~1.41x faster than straight movement
        if direction_x and direction_y:
            target_x *= 0.7071
            target_y *= 0.7071
        self.velocity_x += (target_x - self.velocity_x) * self.SHIP_RESPONSIVENESS
        self.velocity_y += (target_y - self.velocity_y) * self.SHIP_RESPONSIVENESS
        # Drop the tail of the ease-out so the ship actually comes to rest
        if abs(self.velocity_x) < 0.05:
            self.velocity_x = 0
        if abs(self.velocity_y) < 0.05:
            self.velocity_y = 0

        self.spaceship_x += self.velocity_x
        self.spaceship_y += self.velocity_y
        # Keep the 32x32 ship fully on screen, stopping dead against the edges
        if not 0 <= self.spaceship_x <= self.window_width - 32:
            self.spaceship_x = max(0, min(self.window_width - 32, self.spaceship_x))
            self.velocity_x = 0
        if not 0 <= self.spaceship_y <= self.window_height - 32:
            self.spaceship_y = max(0, min(self.window_height - 32, self.spaceship_y))
            self.velocity_y = 0

    def random_spawn_x(self, previous_x=None):
        # Keep consecutive enemies at least two ship widths apart so they don't arrive stacked
        while True:
            x = random.randint(0, self.window_width - 32)
            if previous_x is None or abs(x - previous_x) >= 64:
                return x

    def drop_power_up(self, center):
        self.power_ups.append(PowerUp(self.win, random.choice(POWER_UPS), center, self.font))

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
                self.move_spaceship(keys[controls['right']] - keys[controls['left']],
                                    keys[controls['down']] - keys[controls['up']])
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
                    x = random.randint(0, self.window_width - 32)
                    enemy.set_init(x, -32, random.choice(self.enemy_movement))
                for bullet in self.bullets:
                    if self.collision.check(enemy, bullet, self.explosion):
                        self.score += 10 * self.level
                        self.explosions.append(Explosion(self.win, enemy.hitbox.center))
                        if random.random() < self.POWER_UP_CHANCE:
                            self.drop_power_up(enemy.hitbox.center)
                if self.collision.check(enemy, self.player, self.explosion):
                    self.explosions.append(Explosion(self.win, self.player.hitbox.center, 1.6, 50))
                if self.player.visible and enemy.ready_to_fire():
                    self.enemy_bullets.append(aimed(self.win, enemy.hitbox.midbottom, self.player.hitbox.center,
                                                    self.ENEMY_BULLET_SPEED))

            if self.boss:
                self.handle_boss()

            self.bullets = [bullet for bullet in self.bullets if bullet.visible]

            # Cancel any shots still in flight once the level is cleared, so the player can't die after winning
            if self.level_cleared():
                self.enemy_bullets = []
            for enemy_bullet in self.enemy_bullets:
                enemy_bullet.draw()
                if self.collision.check(enemy_bullet, self.player, self.explosion):
                    self.explosions.append(Explosion(self.win, self.player.hitbox.center, 1.6, 50))
            self.enemy_bullets = [enemy_bullet for enemy_bullet in self.enemy_bullets if enemy_bullet.visible]

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
                self.velocity_x = 0
                self.velocity_y = 0
                self.paused = True
                self.player.lives -= 1
                self.weapon = BLASTER
                self.weapon_timer = 0

            text = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
            self.win.blit(text, (10, 10))
            if self.boss:
                self.boss.draw_health_bar()
            if self.weapon_timer > 0:
                text = self.font.render(f"{self.weapon.name}: {self.weapon_timer // 60 + 1}s", 1, self.weapon.color)
                self.win.blit(text, (10, 35))

    def handle_boss(self):
        boss = self.boss
        boss.draw()
        # Not Collision.check: a bullet hit must only damage the boss, and touching it must not hide it
        for bullet in self.bullets:
            if boss.visible and bullet.visible and bullet.hitbox.colliderect(boss.hitbox):
                bullet.visible = False
                if boss.hit():
                    self.explosion.play()
                    self.score += 100 * self.level
                    self.explosions.append(Explosion(self.win, boss.hitbox.center, 3, 90))
                    self.drop_power_up(boss.hitbox.center)
        if boss.visible and self.player.visible and boss.hitbox.colliderect(self.player.hitbox):
            self.explosion.play()
            self.player.visible = False
            self.explosions.append(Explosion(self.win, self.player.hitbox.center, 1.6, 50))
        if boss.visible and self.player.visible:
            self.enemy_bullets.extend(boss.fire(self.player.hitbox.center))
