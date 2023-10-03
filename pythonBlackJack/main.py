from blackjack.game import Game
import pygame
from blackjack.constants import *
from blackjack.menu import menu


def main():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('blackjack')
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.fill(DARK_GREEN_COLOR)
    pygame.init()

    run = True
    game_flag = False
    game = None
    clock = pygame.time.Clock()
    WIN.blit(background_surface, (0, 0))

    while run:
        clock.tick(FPS)
        pygame.display.update()
        WIN.fill(DARK_GREEN_COLOR)

        if game_flag is False:
            player_amount = 0
            while player_amount == 0:
                player_amount = menu(WIN)
            game = Game(player_amount, 6)
            for p in game.players:
                p.money = 1000
            game_flag = True

        if game_flag is True:
            game_flag = game.new_round(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()


