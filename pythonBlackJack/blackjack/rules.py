import sys

import pygame

from blackjack.constants import GREY, BUTTON_SIZE, WIDTH, HEIGHT, DARK_GREEN_COLOR, GREY_HOVER
from blackjack.graphics import draw_button, write_text

text0 = "the goal is to beat the dealer. If the sum of your cards are more than 21 you automatically lose, meaning you bust."

text01 = "If the sum of your cards are more than the sum of the cards of the dealer or the dealer busts, you win."

text02 = "Stand button - you pass the turn."

text03 = "Hit button - you get a card."

text04 = "Double button - You can do this action only if you have 2 cards. You double your original bet and get a card and pass the turn."

text05 = "Split button - You can do split if your hand has 2 cards that their value are equal to each other - "

text06 = " your hand is split to two hands and the original bet is placed on the other hand."

text1 = "rules specific for this game:"

text2 = """This game uses 6 deck cards. Each deck contains your standard 52 play cards."""

text3 = """There is a red card in the shuffled decks. The red card is placed after 70% to 80% of the total cards."""

text4 = """Once the red card is drawn it signals the dealer to shuffle the decks."""

text5 = """The dealer hits on soft 17."""

text6 = """The maximum number of splits you can do in a round is 3."""

text7 = """Double after a split is allowed."""

text8 = "All players start with 1000 money."

text9 = "If a player has less than 1 money the player is kicked from the game."


def print_rules(window):
    window.fill(DARK_GREEN_COLOR)  # reset board
    write_text(window, (WIDTH // 2, 20), text0, text_font=28)
    write_text(window, (WIDTH // 2, 50), text01, text_font=28)
    write_text(window, (WIDTH // 2, 80), text02, text_font=28)
    write_text(window, (WIDTH // 2, 110), text03, text_font=28)
    write_text(window, (WIDTH // 2, 140), text04, text_font=28)
    write_text(window, (WIDTH // 2, 170), text05, text_font=28)
    write_text(window, (WIDTH // 2, 200), text06, text_font=28)
    write_text(window, (WIDTH // 2, 230), text1, text_font=28)
    write_text(window, (WIDTH // 2, 260), text2, text_font=28)
    write_text(window, (WIDTH // 2, 290), text3, text_font=28)
    write_text(window, (WIDTH // 2, 320), text4, text_font=28)
    write_text(window, (WIDTH // 2, 350), text5, text_font=28)
    write_text(window, (WIDTH // 2, 380), text6, text_font=28)
    write_text(window, (WIDTH // 2, 410), text7, text_font=28)
    write_text(window, (WIDTH // 2, 440), text8, text_font=28)
    write_text(window, (WIDTH // 2, 470), text9, text_font=28)

    center_menu_button = (WIDTH // 2, HEIGHT - 40)

    rules = True
    while rules:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame
                sys.exit()  # Exit the program

            draw_button(window, GREY, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Menu')

            mouse_x, mouse_y = pygame.mouse.get_pos()
            top_left_x = center_menu_button[0] - BUTTON_SIZE[0] / 2
            top_left_y = center_menu_button[1] - BUTTON_SIZE[1] / 2
            if (
                    top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                    and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
            ):
                draw_button(window, DARK_GREEN_COLOR, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Menu')
                draw_button(window, GREY_HOVER, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Menu')
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                    window.fill(DARK_GREEN_COLOR)  # reset board
                    rules = False

        pygame.time.Clock().tick(60)
        pygame.display.update()
