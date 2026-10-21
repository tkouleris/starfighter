import time
from os import path
import pygame


class Menu:

    def __init__(self, high_scores, settings_menu):
        self.high_scores = high_scores
        self.settings_menu = settings_menu
        self.bg = pygame.image.load(path.join('assets', 'menu_bg.png'))
        self.change = pygame.mixer.Sound(path.join('assets', 'sounds', 'change.mp3'))
        settings_menu.settings.register_sound(self.change)
        self.clock = pygame.time.Clock()
        self.running = True
        self.output = 0
        self.selections = [
            (0, 255, 0),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0)
        ]
        self.select = 0
        self.rect = pygame.Rect(200, 270, 200, 185)
        self.font = pygame.font.SysFont('comicsans', 30, True, True)
        self.small_font = pygame.font.SysFont('comicsans', 20, True, True)

    def handle(self):

        while self.running:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.change.play()
                        temp_selection = self.select
                        selection_color_tmp = self.selections[self.select]
                        self.select += 1
                        self.select = self.select % len(self.selections)
                        not_selection_color = self.selections[self.select]
                        self.selections[self.select] = selection_color_tmp
                        self.selections[temp_selection] = not_selection_color
                    if event.key == pygame.K_UP:
                        self.change.play()
                        temp_selection = self.select
                        selection_color_tmp = self.selections[self.select]
                        self.select -= 1
                        self.select = self.select % len(self.selections)
                        not_selection_color = self.selections[self.select]
                        self.selections[self.select] = selection_color_tmp
                        self.selections[temp_selection] = not_selection_color
                    if event.key == pygame.K_RETURN:
                        self.change.play()
                        time.sleep(1)
                        match self.select:
                            case 0:
                                return
                            case 1:
                                self.show_high_scores()
                            case 2:
                                self.settings_menu.handle()
                            case 3:
                                pygame.quit()
                                exit()


            screen = pygame.display.get_surface()
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
            font = self.font
            text = font.render("Start ", 1, self.selections[0])
            screen.blit(text, (300 - (text.get_width() / 2), 280))
            text = font.render("High Scores ", 1, self.selections[1])
            screen.blit(text, (300 - (text.get_width() / 2), 322))
            text = font.render("Settings ", 1, self.selections[2])
            screen.blit(text, (300 - (text.get_width() / 2), 364))
            text = font.render("Quit ", 1, self.selections[3])
            screen.blit(text, (300 - (text.get_width() / 2), 406))

            pygame.display.update()

    def show_high_scores(self):
        while True:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYUP and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.change.play()
                    return

            screen = pygame.display.get_surface()
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 40, 340, 420))
            self.high_scores.draw(screen, 50)
            font = self.small_font
            text = font.render("Press Enter to return", 1, (255, 0, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 420))

            pygame.display.update()
