import time
import pygame
from game import Game
from high_scores import HighScores
from menu import Menu


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game(1)
    high_scores = HighScores()
    menu = Menu(high_scores)

    menu.handle()

    name_entry = None
    score_recorded = False

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif name_entry is not None:
                    if event.key == pygame.K_BACKSPACE:
                        name_entry = name_entry[:-1]
                    elif event.key == pygame.K_RETURN and len(name_entry) > 0:
                        high_scores.add(name_entry, game.score)
                        name_entry = None
                        score_recorded = True
                    elif event.unicode.isalpha() and len(name_entry) < 3:
                        name_entry += event.unicode.upper()
            if event.type == pygame.KEYUP:
                if game.paused and game.player.lives > 0 and event.key == pygame.K_SPACE:
                    time.sleep(2)
                    game.init_game()
                if game.paused and game.player.lives <= 0 and score_recorded and event.key == pygame.K_y:
                    game.player.lives = 3
                    game.level = 1
                    game.score = 0
                    score_recorded = False
                    game.init_game()
                if game.paused and game.player.lives <= 0 and score_recorded and event.key == pygame.K_n:
                    running = False

        game.handle()
        visible_enemies = [enemy.visible for enemy in game.enemies]
        if not any(visible_enemies) and game.paused is False:
            game.paused = True
            game.level += 1

        if game.paused and game.player.lives > 0:
            clock.tick(5)
            screen = pygame.display.set_mode((640, 480))
            font = pygame.font.SysFont('comicsans', 30, True, True)
            text = font.render("Lives: " + str(game.player.lives), 1, (255, 0, 0))
            screen.blit(text, (250 - (text.get_width() / 2), 200))
            text = font.render("Level " + str(game.level), 1, (255, 0, 0))
            screen.blit(text, (250 - (text.get_width() / 2), 250))
            text = font.render("Score: " + str(game.score), 1, (255, 0, 0))
            screen.blit(text, (250 - (text.get_width() / 2), 300))

        if game.paused and game.player.lives <= 0:
            if not score_recorded and name_entry is None:
                if high_scores.qualifies(game.score):
                    name_entry = ''
                else:
                    score_recorded = True

            clock.tick(5)
            screen = pygame.display.set_mode((640, 480))
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('comicsans', 30, True, True)
            text = font.render("GAME OVER", 1, (255, 0, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 10))
            text = font.render("Score: " + str(game.score), 1, (255, 0, 0))
            screen.blit(text, (320 - (text.get_width() / 2), 50))

            if name_entry is not None:
                text = font.render("NEW HIGH SCORE!", 1, (255, 255, 0))
                screen.blit(text, (320 - (text.get_width() / 2), 180))
                text = font.render("Enter initials: " + name_entry.ljust(3, '_'), 1, (255, 255, 255))
                screen.blit(text, (320 - (text.get_width() / 2), 240))
                text = font.render("(Enter to confirm)", 1, (255, 255, 255))
                screen.blit(text, (320 - (text.get_width() / 2), 300))
            else:
                high_scores.draw(screen, 100)
                text = font.render("Play again (y/n)", 1, (255, 0, 0))
                screen.blit(text, (320 - (text.get_width() / 2), 430))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
