import time
import pygame
from game import Game
from menu import Menu


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = Game(1)
    menu = Menu()

    menu.handle()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:
                if game.paused and game.player.lives > 0 and event.key == pygame.K_SPACE:
                    time.sleep(2)
                    game.init_game()
                if game.paused and game.player.lives <= 0 and event.key == pygame.K_y:
                    game.player.lives = 3
                    game.level = 1
                    game.init_game()
                if game.paused and game.player.lives <= 0 and event.key == pygame.K_n:
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

        if game.paused and game.player.lives <= 0:
            clock.tick(5)
            screen = pygame.display.set_mode((640, 480))
            font = pygame.font.SysFont('comicsans', 30, True, True)
            text = font.render("GAME OVER", 1, (255, 0, 0))
            screen.blit(text, (250 - (text.get_width() / 2), 200))
            text = font.render("Play again (y/n)", 1, (255, 0, 0))
            screen.blit(text, (250 - (text.get_width() / 2), 250))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
