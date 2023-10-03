import os
import sys

import pygame
import time
from blackjack.constants import TEXT_INFO_POS, WIDTH, CARD_SIZE, SEAT_ONE_FIRST_POS, DEALER_FIRST_POS, \
    SEAT_TWO_FIRST_POS, SEAT_THREE_FIRST_POS, SEAT_FOUR_FIRST_POS, NEXT_CARD_ADJUSTMENT_FACTOR, RED, FONT_NUMBER, GREY, \
    STAND_BUTTON_POS, BUTTON_SIZE, HIT_BUTTON_POS, DOUBLE_BUTTON_POS, SPLIT_BUTTON_POS, DARK_GREEN_COLOR, HEIGHT, \
    CARD_ONE_SPILT_POS, CARD_TWO_SPILT_POS, CARD_THREE_SPILT_POS, CARD_FOUR_SPILT_POS, BLACK, TEXT_PLAYER1_BET_POS, \
    TEXT_PLAYER2_BET_POS, TEXT_PLAYER3_BET_POS, TEXT_PLAYER4_BET_POS, GREY_HOVER
from blackjack.graphics import write_text, draw_rotated_rectangle, draw_card, draw_button

BLACKJACK_VALUE = 21
MAX_SPLITS = 3


class Player:
    def __init__(self, player_num):
        self.player_num = player_num
        self.cards = []
        self.total_value = 0
        self.another_total_value = 0
        self.actions = {'stand': True, 'hit': True, 'double': False, 'split': False}
        self.money = 0
        self.bet = 0
        self.last_bet = 0
        self.split = None
        self.number_of_splits = 0
        self.win = 0
        self.blackjack = False
        self.max_value = False
        self.bust = False
        self.father = None
        self.sons = []
        self.card_pos = [self.set_graphics_attributes(), 0]  # (first position, increment)
        self.card_split_pos = self.set_split_graphics()  # first position
        self.turn = False

    def go_to_menu(self, window, event):
        center_menu_button = (WIDTH // 2, HEIGHT - 40)
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
                return True
        return False

    def set_graphics_attributes(self):
        if self.player_num == 0:
            return DEALER_FIRST_POS
        elif self.player_num == 1:
            return SEAT_ONE_FIRST_POS
        elif self.player_num == 2:
            return SEAT_TWO_FIRST_POS
        elif self.player_num == 3:
            return SEAT_THREE_FIRST_POS
        elif self.player_num == 4:
            return SEAT_FOUR_FIRST_POS

    def set_split_graphics(self):
        if self.player_num == 0:
            return None
        elif self.player_num == 1:
            return CARD_ONE_SPILT_POS
        elif self.player_num == 2:
            return CARD_TWO_SPILT_POS
        elif self.player_num == 3:
            return CARD_THREE_SPILT_POS
        elif self.player_num == 4:
            return CARD_FOUR_SPILT_POS

    def add_card(self, card, window):
        time.sleep(0.5)

        # play sound
        # Get the current directory (folder 'a' in this case)
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the path to folder 'b'
        folder_sounds_path = os.path.join(os.path.dirname(current_directory), 'sounds')

        # Now, you can access files in folder 'b' using folder_b_path
        file_in_sounds_path = os.path.join(folder_sounds_path, 'add_card_sound.wav')

        # playing the sound
        add_card_sound = pygame.mixer.Sound(file_in_sounds_path)
        add_card_sound.set_volume(0.2)
        add_card_sound.play()

        self.cards += [card]

        if self.player_num == 0 and len(self.cards) == 1:  # the case the first card for the dealer
            draw_button(window, RED, (self.card_pos[0][0] + self.card_pos[1], self.card_pos[0][1]),
                        CARD_SIZE[0], CARD_SIZE[1], '')
        elif len(card) == 2:  # the case card = '10'
            draw_card(card, window, CARD_SIZE[0], CARD_SIZE[1],
                      (self.card_pos[0][0] + self.card_pos[1], self.card_pos[0][1]))
        else:
            draw_card(card[0], window, CARD_SIZE[0], CARD_SIZE[1],
                      (self.card_pos[0][0] + self.card_pos[1], self.card_pos[0][1]))
        self.card_pos[1] += NEXT_CARD_ADJUSTMENT_FACTOR
        pygame.time.Clock().tick(60)
        pygame.display.update()

        if card == 'Jack' or card == 'Queen' or card == 'King':
            self.total_value += 10
            self.another_total_value += 10
        elif card == 'Ace':
            self.total_value += 1
            self.another_total_value = self.total_value + 10
        else:
            self.total_value += int(card)
            self.another_total_value += int(card)
        if self.another_total_value > 21:
            self.another_total_value = 0
        if self.total_value > 21:
            self.bust = True
        elif len(self.cards) == 2 and self.get_higher_value() == 21 and self.father is None:
            self.blackjack = True

        # higher sum for players
        if self.player_num != 0:
            self.print_sum(window, 90)

    def print_sum(self, window, y_factor):
        pos_x = self.card_pos[0][0]
        pos_y = self.card_pos[0][1] + CARD_SIZE[1] + y_factor
        pos = (pos_x, pos_y)
        draw_rotated_rectangle(window, DARK_GREEN_COLOR, pos, 150, FONT_NUMBER * 1.5, 0)  # clear text
        write_text(window, pos, f"cards sum: {self.get_higher_value()}")  # print sum
        pygame.time.Clock().tick(60)
        pygame.display.update()

    def reset_player(self):
        self.cards = []
        self.total_value = 0
        self.another_total_value = 0
        self.actions = {'stand': True, 'hit': True, 'double': False, 'split': False}
        self.bet = 0
        self.split = None
        self.number_of_splits = 0
        self.win = False
        self.blackjack = False
        self.max_value = False
        self.bust = False
        self.father = None
        self.sons = []
        self.card_pos = [self.set_graphics_attributes(), 0]  # (first position, increment)
        self.card_split_pos = self.set_split_graphics()  # first position
        self.turn = False

    def decide_action(self, window):
        draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
        draw_rotated_rectangle(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, WIDTH, BUTTON_SIZE[1], 0)  # clear buttons
        while True:
            self.actions['double'] = False
            self.actions['split'] = False
            if len(self.cards) == 2 and self.money >= self.bet:
                self.actions['double'] = True
                if self.get_root_player().number_of_splits < MAX_SPLITS:
                    if self.cards[0] == self.cards[1]:
                        self.actions['split'] = True
                    elif len(self.cards[0]) >= 2 and len(self.cards[1]) >= 2:  # if both cards are of a value 10
                        self.actions['split'] = True

            cards_and_sum = f"cards: {self.cards} sum: {self.get_higher_value()}"
            action_msg = cards_and_sum + "\n" + f"player {self.player_num} please choose an action:"
            keys = self.actions.keys()
            for key in keys:
                if self.actions[key] is True:
                    action_msg += " " + key
            print(action_msg)
            # write text info for player and draw buttons
            write_text(window, TEXT_INFO_POS, f"player {self.player_num} please choose an action:", text_font=40)
            draw_button(window, GREY, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Stand')
            draw_button(window, GREY, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Hit')
            if self.actions['double'] is True:
                draw_button(window, GREY, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Double')
            if self.actions['split'] is True:
                draw_button(window, GREY, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Split')
            pygame.time.Clock().tick(60)
            pygame.display.update()

            #action = input()
            action = ''
            # check the player mouse click on which button
            decide = True
            while decide:
                pygame.time.Clock().tick(60)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # Quit Pygame
                        sys.exit()  # Exit the program

                    if self.go_to_menu(window, event) is True:
                        return 'go_to_menu'
                    pygame.time.Clock().tick(60)
                    pygame.display.update()

                    # clearing the buttons and drawing them again
                    draw_rotated_rectangle(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, WIDTH, BUTTON_SIZE[1],
                                           0)  # clear buttons
                    if self.actions['stand'] is True:
                        draw_button(window, GREY, STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Stand')
                    if self.actions['hit'] is True:
                        draw_button(window, GREY, HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Hit')
                    if self.actions['double'] is True:
                        draw_button(window, GREY, DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Double')
                    if self.actions['split'] is True:
                        draw_button(window, GREY, SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Split')

                    # highlighting the button when mouse hover
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    highlight = self.clicked_action(mouse_x, mouse_y)
                    if highlight == 'stand' and self.actions['stand'] is True:
                        draw_rotated_rectangle(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, BUTTON_SIZE[0],
                                               BUTTON_SIZE[1], 0)  # clear button
                        draw_button(window, (50, 50, 50), STAND_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Stand')
                    elif highlight == 'hit' and self.actions['hit'] is True:
                        draw_rotated_rectangle(window, DARK_GREEN_COLOR, HIT_BUTTON_POS, BUTTON_SIZE[0],
                                               BUTTON_SIZE[1], 0)  # clear button
                        draw_button(window, (50, 50, 50), HIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Hit')
                    elif highlight == 'double' and self.actions['double'] is True:
                        draw_rotated_rectangle(window, DARK_GREEN_COLOR, DOUBLE_BUTTON_POS, BUTTON_SIZE[0],
                                               BUTTON_SIZE[1], 0)  # clear button
                        draw_button(window, (50, 50, 50), DOUBLE_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Double')
                    elif highlight == 'split' and self.actions['split'] is True:
                        draw_rotated_rectangle(window, DARK_GREEN_COLOR, SPLIT_BUTTON_POS, BUTTON_SIZE[0],
                                               BUTTON_SIZE[1], 0)  # clear button
                        draw_button(window, (50, 50, 50), SPLIT_BUTTON_POS, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Split')

                    pygame.time.Clock().tick(60)
                    pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        action = self.clicked_action(mouse_x, mouse_y)
                        if action is not None:
                            decide = False

            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, STAND_BUTTON_POS, WIDTH, BUTTON_SIZE[1],
                                   0)  # clear buttons

            action = action.lower()

            pygame.time.Clock().tick(60)
            pygame.display.update()

            for key in keys:
                if action == key and self.actions[key] is True:
                    return action
            print("Please choose an action that is listed")

    def clicked_action(self, mouse_x, mouse_y):
        top_left_x = STAND_BUTTON_POS[0] - BUTTON_SIZE[0] / 2
        top_left_y = STAND_BUTTON_POS[1] - BUTTON_SIZE[1] / 2
        if (
                top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
        ):
            return 'stand'
        top_left_x = HIT_BUTTON_POS[0] - BUTTON_SIZE[0] / 2
        top_left_y = HIT_BUTTON_POS[1] - BUTTON_SIZE[1] / 2
        if (
                top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
        ):
            return 'hit'
        top_left_x = DOUBLE_BUTTON_POS[0] - BUTTON_SIZE[0] / 2
        top_left_y = DOUBLE_BUTTON_POS[1] - BUTTON_SIZE[1] / 2
        if (
                top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
        ):
            return 'double'
        top_left_x = SPLIT_BUTTON_POS[0] - BUTTON_SIZE[0] / 2
        top_left_y = SPLIT_BUTTON_POS[1] - BUTTON_SIZE[1] / 2
        if (
                top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
        ):
            return 'split'
        return None

    def check_player_bust(self):
        if self.total_value > BLACKJACK_VALUE:
            return True
        return False

    def place_bet(self, window):
        while True:
            print(f"player {self.player_num} you have {self.money} money")
            print(f"player {self.player_num} please place a bet:")
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, 40 * 2, 0)  # clear text
            write_text(window, TEXT_INFO_POS, f"Please type your bet and press enter:", text_font=40)
            text = f"Player {self.player_num} has {self.money} money."
            if self.last_bet != 0:
                text += f"Your last original bet is {self.last_bet}"
            write_text(window, (TEXT_INFO_POS[0], TEXT_INFO_POS[1] - 60), text, text_font=40)
            pygame.time.Clock().tick(60)
            pygame.display.update()
            #bet = input()
            bet = ''

            input_active = True
            input_text = ""

            while input_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    center_menu_button = (WIDTH // 2, HEIGHT - 320)
                    if self.last_bet != 0:
                        draw_button(window, GREY, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Same bet')
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        top_left_x = center_menu_button[0] - BUTTON_SIZE[0] / 2
                        top_left_y = center_menu_button[1] - BUTTON_SIZE[1] / 2
                        if (
                                top_left_x < mouse_x < top_left_x + BUTTON_SIZE[0]
                                and top_left_y < mouse_y < top_left_y + BUTTON_SIZE[1]
                        ):
                            draw_button(window, DARK_GREEN_COLOR, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1],
                                        'Same bet')
                            draw_button(window, GREY_HOVER, center_menu_button, BUTTON_SIZE[0], BUTTON_SIZE[1], 'Same bet')
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                                window.fill(DARK_GREEN_COLOR)  # reset board
                                input_text = str(self.last_bet)
                                input_active = False
                                break

                    exit_to_menu_flag = self.go_to_menu(window, event)
                    if exit_to_menu_flag is True:
                        return False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode

                draw_rotated_rectangle(window, DARK_GREEN_COLOR, (WIDTH // 2, HEIGHT // 2), WIDTH, 26 * 2, 0)
                text_surface = pygame.font.Font(None, 40).render("" +
                                                                 input_text, True, BLACK)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                window.blit(text_surface, text_rect)

                pygame.time.Clock().tick(60)
                pygame.display.update()
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, (WIDTH // 2, HEIGHT // 2), WIDTH, 26 * 2, 0)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, (WIDTH // 2, HEIGHT - 320), BUTTON_SIZE[0], BUTTON_SIZE[1], 0)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, (TEXT_INFO_POS[0], TEXT_INFO_POS[1] - 60), WIDTH, 26 * 2, 0)
            window.fill(DARK_GREEN_COLOR)
            pygame.time.Clock().tick(60)
            pygame.display.update()

            bet = input_text
            if bet.isdigit() is False:
                print(f"player {self.player_num} please enter digits only for the bet. please try again")
                draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
                write_text(window, TEXT_INFO_POS,
                           f"player {self.player_num} please enter digits only for the bet. please try again", text_font=40)
                pygame.time.Clock().tick(60)
                pygame.display.update()
                time.sleep(2)  # Pause for 2 seconds
                continue
            if self.money - int(bet) < 0:
                print(f"player {self.player_num} you can't place a bet more than your money. please try again.")
                draw_rotated_rectangle(window, (0, 100, 0), TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
                write_text(window, TEXT_INFO_POS,
                           f"player {self.player_num} you can't place a bet more than your money. please try again.", text_font=40)
                pygame.time.Clock().tick(60)
                pygame.display.update()
                time.sleep(2)  # Pause for 2 seconds
                continue
            if int(bet) == 0:
                print(f"player {self.player_num} you can't place zero as a bet.")
                draw_rotated_rectangle(window, (0, 100, 0), TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
                write_text(window, TEXT_INFO_POS,
                           f"player {self.player_num} you can't place zero as a bet.", text_font=40)
                pygame.time.Clock().tick(60)
                pygame.display.update()
                time.sleep(2)  # Pause for 2 seconds
                continue
            self.bet = int(bet)
            self.money -= self.bet
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
            self.last_bet = self.bet
            return True

    def split_copy(self, other, split_num):
        other.player_num = self.player_num
        other.cards = [self.cards[split_num]]
        other.total_value = self.total_value // 2
        other.another_total_value = self.total_value // 2
        if other.total_value == 1:
            other.another_total_value = 11  # the split was with aces
        other.actions = {'stand': True, 'hit': True, 'double': False, 'split': False}
        other.money = self.money - self.bet
        other.bet = self.bet
        other.split = None
        other.win = 0
        other.blackjack = False
        other.max_value = False
        other.bust = False
        other.father = self
        other.sons = []
        self.card_pos = [self.set_graphics_attributes(), 0]  # (first position, increment)
        self.card_split_pos = self.set_split_graphics()  # (first position, increment)
        other.turn = self.turn

    def get_root_player(self):
        if self.father is None:
            return self
        return self.father.get_root_player()

    def set_sons_player_list(self):
        if self.split is None:
            self.get_root_player().sons += [self]
            return
        self.split[0].set_sons_player_list()
        self.split[1].set_sons_player_list()

    def get_higher_value(self):
        if self.total_value > self.another_total_value:
            return self.total_value
        return self.another_total_value
