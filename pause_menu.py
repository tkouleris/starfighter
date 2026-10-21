from os import path
import pygame


class PauseMenu:
    RESUME = 'resume'
    SETTINGS = 'settings'
    MAIN_MENU = 'menu'
    QUIT = 'quit'

    def __init__(self, settings_menu):
        self.settings_menu = settings_menu
        self.change = pygame.mixer.Sound(path.join('assets', 'sounds', 'change.mp3'))
        settings_menu.settings.register_sound(self.change)
        self.clock = pygame.time.Clock()
        self.options = [("Resume", self.RESUME), ("Settings", self.SETTINGS), ("Main Menu", self.MAIN_MENU), ("Quit", self.QUIT)]
        self.title_font = pygame.font.SysFont('comicsans', 40, True, True)
        self.font = pygame.font.SysFont('comicsans', 30, True, True)
        self.rect = pygame.Rect(200, 110, 240, 270)

    def handle(self):
        screen = pygame.display.get_surface()
        background = screen.copy()
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        select = 0

        while True:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.QUIT
                # Esc/P resume on KEYDOWN so the KEYUP of the key that opened the menu is ignored
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                    return self.RESUME
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.change.play()
                        select = (select + 1) % len(self.options)
                    if event.key == pygame.K_UP:
                        self.change.play()
                        select = (select - 1) % len(self.options)
                    if event.key == pygame.K_RETURN:
                        self.change.play()
                        if self.options[select][1] == self.SETTINGS:
                            self.settings_menu.handle()
                        else:
                            return self.options[select][1]

            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
            text = self.title_font.render("PAUSED", 1, (255, 255, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 125))
            for index, (label, _) in enumerate(self.options):
                color = (0, 255, 0) if index == select else (255, 0, 0)
                text = self.font.render(label, 1, color)
                screen.blit(text, (320 - (text.get_width() / 2), 190 + index * 45))

            pygame.display.update()
