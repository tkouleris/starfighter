import time
from os import path
import pygame


class Menu:

    def __init__(self, high_scores):
        self.high_scores = high_scores
        self.bg = pygame.image.load(path.join('assets', 'menu_bg.png'))
        self.change = pygame.mixer.Sound(path.join('assets', 'sounds', 'change.mp3'))
        self.clock = pygame.time.Clock()
        self.running = True
        self.output = 0
        self.selections = [
            (0, 255, 0),
            (255, 0, 0),
            (255, 0, 0)
        ]
        self.select = 0
        self.rect = pygame.Rect(200, 290, 200, 140)

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
                                pygame.quit()
                                exit()


            screen = pygame.display.set_mode((640, 480))
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), self.rect)
            font = pygame.font.SysFont('comicsans', 30, True, True)
            text = font.render("Start ", 1, self.selections[0])
            screen.blit(text, (300 - (text.get_width() / 2), 300))
            text = font.render("High Scores ", 1, self.selections[1])
            screen.blit(text, (300 - (text.get_width() / 2), 345))
            text = font.render("Quit ", 1, self.selections[2])
            screen.blit(text, (300 - (text.get_width() / 2), 390))

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

            screen = pygame.display.set_mode((640, 480))
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 40, 340, 420))
            self.high_scores.draw(screen, 50)
            font = pygame.font.SysFont('comicsans', 20, True, True)
            text = font.render("Press Enter to return", 1, (255, 0, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 420))

            pygame.display.update()
