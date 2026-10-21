from os import path
import pygame
from settings import Settings


class SettingsMenu:
    BACK = 'back'
    VOLUMES = ('music', 'sfx')

    def __init__(self, settings):
        self.settings = settings
        self.change = pygame.mixer.Sound(path.join('assets', 'sounds', 'change.mp3'))
        settings.register_sound(self.change)
        self.clock = pygame.time.Clock()
        self.options = [('music', "Music"), ('sfx', "Sound FX")] + Settings.ACTIONS + [(self.BACK, "Back")]
        self.title_font = pygame.font.SysFont('comicsans', 40, True, True)
        self.font = pygame.font.SysFont('comicsans', 24, True, True)
        self.small_font = pygame.font.SysFont('comicsans', 18, True, True)
        self.rect = pygame.Rect(100, 30, 440, 420)

    def handle(self):
        screen = pygame.display.get_surface()
        background = screen.copy()
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        select = 0
        waiting = False
        # The KEYUP of a freshly bound key must not also navigate the menu
        ignore_keyup = None

        while True:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                option = self.options[select][0]
                if waiting:
                    # P is reserved for opening the pause menu during play
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_p:
                        if event.key != pygame.K_ESCAPE:
                            self.settings.bind(option, event.key)
                        self.change.play()
                        waiting = False
                        ignore_keyup = event.key
                    continue
                if event.type == pygame.KEYUP:
                    if event.key == ignore_keyup:
                        ignore_keyup = None
                        continue
                    if event.key == pygame.K_DOWN:
                        self.change.play()
                        select = (select + 1) % len(self.options)
                    if event.key == pygame.K_UP:
                        self.change.play()
                        select = (select - 1) % len(self.options)
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT) and option in self.VOLUMES:
                        self.settings.adjust_volume(option, 1 if event.key == pygame.K_RIGHT else -1)
                        self.change.play()
                    if event.key == pygame.K_RETURN and option not in self.VOLUMES:
                        self.change.play()
                        if option == self.BACK:
                            return
                        waiting = True
                    if event.key == pygame.K_ESCAPE:
                        self.change.play()
                        return

            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
            text = self.title_font.render("SETTINGS", 1, (255, 255, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 40))

            for index, (option, label) in enumerate(self.options):
                y = 105 + index * 36
                color = (0, 255, 0) if index == select else (255, 0, 0)
                text = self.font.render(label, 1, color)
                if option == self.BACK:
                    screen.blit(text, (320 - (text.get_width() / 2), y))
                elif option in self.VOLUMES:
                    screen.blit(text, (self.rect.x + 30, y))
                    volume = self.settings.music_volume if option == 'music' else self.settings.sfx_volume
                    for step in range(Settings.MAX_VOLUME):
                        box = pygame.Rect(self.rect.right - 150 + step * 12, y + 10, 10, 16)
                        pygame.draw.rect(screen, color if step < volume else (60, 60, 60), box)
                else:
                    screen.blit(text, (self.rect.x + 30, y))
                    if waiting and index == select:
                        value = self.font.render("Press a key...", 1, (255, 255, 0))
                    else:
                        value = self.font.render(pygame.key.name(self.settings.controls[option]).upper(), 1,
                                                 (255, 255, 255))
                    screen.blit(value, (self.rect.right - 30 - value.get_width(), y))

            hint = "Esc to cancel" if waiting else "Left/Right: volume   Enter: rebind   Esc: back"
            text = self.small_font.render(hint, 1, (255, 255, 255))
            screen.blit(text, (320 - (text.get_width() / 2), 415))

            pygame.display.update()
