import sys

import pygame

from blackjack.constants import GREY, STAND_BUTTON_POS, BUTTON_SIZE, DARK_GREEN_COLOR, TEXT_INFO_POS, HIT_BUTTON_POS, \
    DOUBLE_BUTTON_POS, SPLIT_BUTTON_POS, CARD_SIZE, NEXT_CARD_ADJUSTMENT_FACTOR, GREY_HOVER, BLACK, WIDTH, HEIGHT
from blackjack.graphics import draw_button, write_text, draw_card
from blackjack.player import Player
from blackjack.rules import print_rules


def menu(window):
    window.fill(DARK_GREEN_COLOR)  # reset board
    write_text(window, TEXT_INFO_POS, 'BLACKJACK     ', text_font=60)
    center = (TEXT_INFO_POS[0] + 150, TEXT_INFO_POS[1])
    draw_card('J', window, CARD_SIZE[0], CARD_SIZE[1], center)
    center = (center[0] + NEXT_CARD_ADJUSTMENT_FACTOR, center[1])
    draw_card('A', window, CARD_SIZE[0], CARD_SIZE[1], center)

    action = ''
    p = Player(-1)
    back_to_menu_flag = False

    # check the player mouse click on which button
    decide = True
    while decide:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame
                sys.exit()  # Exit the program

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover = p.clicked_action(mouse_x, mouse_y)

            draw_button(window, GREY, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'New Game')
            #draw_button(window, GREY, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Make server')
            #draw_button(window, GREY, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Join server')
            draw_button(window, GREY, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Rules')

            # highlighting the button when mouse hover
            if hover == 'stand':
                draw_button(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'New Game')
            elif hover == 'hit':
                pass
                #draw_button(window, DARK_GREEN_COLOR, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                #draw_button(window, GREY_HOVER, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Make server')
            elif hover == 'double':
                pass
                #draw_button(window, DARK_GREEN_COLOR, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                #draw_button(window, GREY_HOVER, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Join server')
            elif hover == 'split':
                draw_button(window, DARK_GREEN_COLOR, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Rules')

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                action = p.clicked_action(mouse_x, mouse_y)
                if action == 'stand':  # 'stand' is 'Local game'
                    decide = False
                elif hover == 'hit':   # 'hit' is 'Make Server'
                    pass
                elif hover == 'double':  # 'double' is 'Join server'
                    pass
                elif action == 'split':  # 'split' is 'Rules'
                    print_rules(window)
                    back_to_menu_flag = True
                    decide = False

        pygame.time.Clock().tick(60)
        pygame.display.update()

    window.fill(DARK_GREEN_COLOR)  # reset board

    if back_to_menu_flag is True:
        return 0

    write_text(window, TEXT_INFO_POS, "choose the amount of players:", text_font=40)

    center_menu_button = (WIDTH // 2, HEIGHT - 40)
    amount_of_players = 0
    decide = True
    while decide:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame
                sys.exit()  # Exit the program

            # return to menu button
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
                    return 0

            # other buttons
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover = p.clicked_action(mouse_x, mouse_y)

            draw_button(window, GREY, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '1')
            draw_button(window, GREY, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '2')
            draw_button(window, GREY, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '3')
            draw_button(window, GREY, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '4')

            # highlighting the button when mouse hover
            if hover == 'stand':
                draw_button(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '1')
            elif hover == 'hit':
                draw_button(window, DARK_GREEN_COLOR, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '2')
            elif hover == 'double':
                draw_button(window, DARK_GREEN_COLOR, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '3')
            elif hover == 'split':
                draw_button(window, DARK_GREEN_COLOR, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '')
                draw_button(window, GREY_HOVER, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], '4')

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                action = p.clicked_action(mouse_x, mouse_y)
                if action == 'stand':  # 'stand' is '1'
                    amount_of_players = 1
                    decide = False
                if action == 'hit':  # 'hit' is '2'
                    amount_of_players = 2
                    decide = False
                if action == 'double':  # 'double' is '3'
                    amount_of_players = 3
                    decide = False
                if action == 'split':  # 'split' is '4'
                    amount_of_players = 4
                    decide = False

        pygame.time.Clock().tick(60)
        pygame.display.update()

    window.fill(DARK_GREEN_COLOR)  # reset board

    return amount_of_players
