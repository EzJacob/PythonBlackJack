import pygame
import time

from blackjack.constants import TEXT_INFO_POS, DARK_GREEN_COLOR, CARD_SIZE, NEXT_CARD_ADJUSTMENT_FACTOR, WIDTH, \
    FONT_NUMBER, CARD_SPLIT_SIZE, CARD_ONE_SPILT_POS, NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR, TEXT_PLAYER1_POS, \
    TEXT_PLAYER2_POS, TEXT_PLAYER3_POS, TEXT_PLAYER4_POS, TEXT_DEALER_POS, TEXT_PLAYER1_BET_POS, TEXT_PLAYER2_BET_POS, \
    TEXT_PLAYER3_BET_POS, TEXT_PLAYER4_BET_POS
from blackjack.deck import Deck
from blackjack.graphics import write_text, draw_rotated_rectangle, draw_card
from blackjack.player import Player
from blackjack.dealer import Dealer


class Game:
    def __init__(self, players_amount, decks_amount):
        self.players_amount = players_amount
        self.deck = Deck(decks_amount)
        self.players = [Player(i) for i in range(1, players_amount + 1)]
        self.dealer = Dealer()
        self.cards_used = 0
        self.split_counter = 0

    def check_for_red_card(self):
        if self.cards_used >= self.deck.red_card_index:
            self.cards_used = 0
            return True
        return False

    def placing_bets(self, window):
        for p in self.players:
            flag_to_menu = p.place_bet(window)
            if flag_to_menu is False:
                return False
        return True

    def action(self, player, action, window):

        # shuffle the deck without the cards that are currently on board
        if self.check_for_red_card() is True:
            cards_playing = self.dealer.dealer.cards
            for p in self.players:
                cards_playing += p.cards
            self.cards_used = len(cards_playing)
            self.deck.shuffle_without_cards_used(cards_playing)
            print("deck reshuffled")
            print(self.deck.deck)
            print(cards_playing)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, 45, 0)
            write_text(window, TEXT_INFO_POS, "Red card was drawn. Deck reshuffled", text_font=30)
            pygame.time.Clock().tick(60)
            pygame.display.update()
            time.sleep(2)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, 45, 0)

        if action == 'stand':
            return False
        elif action == 'hit' or action == 'double':
            player.add_card(self.deck.deck.pop(0), window)
            self.cards_used += 1
            if action == 'double':
                p = player.get_root_player()
                p.money -= p.bet
                player.bet *= 2

                center = (p.card_pos[0][0], p.card_pos[0][1]+ CARD_SIZE[1] + 60)
                draw_rotated_rectangle(window, DARK_GREEN_COLOR, center, 150, FONT_NUMBER * 1.5, 0)  # clear text
                write_text(window, center, f"money: {p.money}")
                return False
            return True
        elif action == 'split':
            p = player.get_root_player()
            p.money -= p.bet
            p.number_of_splits += 1
            x = Player(p.player_num)
            y = Player(p.player_num)
            player.split_copy(x, 0)
            player.split_copy(y, 1)
            player.split = (x, y)

            center = (p.card_pos[0][0], p.card_pos[0][1] + CARD_SIZE[1] + 60)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, center, 150, FONT_NUMBER * 1.5, 0)  # clear text
            write_text(window, center, f"money: {p.money}")
            return True

    def action_phase(self, players, window):
        for p in players:

            if p.father is not None:
                draw_rotated_rectangle(window, DARK_GREEN_COLOR, p.card_pos[0], CARD_SIZE[0] * 4, CARD_SIZE[1],
                                       0)  # clear cards
                card_value = p.cards[0][0]
                if p.cards[0] == '10':
                    card_value = p.cards[0]
                draw_card(card_value, window, CARD_SIZE[0], CARD_SIZE[1], p.card_pos[0])
                p.card_pos[1] += NEXT_CARD_ADJUSTMENT_FACTOR
                pygame.time.Clock().tick(60)
                pygame.display.update()
            else:
                self.split_counter = 0

            if len(p.cards) < 2:  # the case the player has one card from a split
                p.add_card(self.deck.deck.pop(0), window)
                self.cards_used += 1
            while True:
                if p.bust is True or p.blackjack is True:
                    print(f"player {p.player_num} cards:", end=' ')
                    print(p.cards, end=' ')
                    print(f"sum: {p.get_higher_value()}")
                    if p.bust is True:
                        print("this hand is busted")
                    elif p.blackjack is True:
                        print("this hand has a Blackjack!")
                    self.place_split_cards_at_bottom(p, window)
                    break
                if p.get_higher_value() == 21:
                    print(f"player {p.player_num} cards:", end=' ')
                    print(p.cards, end=' ')
                    print(f"sum: {p.get_higher_value()}")
                    self.place_split_cards_at_bottom(p, window)
                    break
                action = p.decide_action(window)
                if action == 'go_to_menu':
                    return False
                if self.action(p, action, window) is False:
                    print(f"player {p.player_num} cards:", end=' ')
                    print(p.cards, end=' ')
                    print(f"sum: {p.get_higher_value()}")
                    if p.bust is True:
                        print("this hand is busted")
                    self.place_split_cards_at_bottom(p, window)
                    break
                if action == 'split':
                    if self.action_phase(p.split, window) is False:
                        return False
                    break
        return True

    def place_split_cards_at_bottom(self, player, window):
        if player.father is None:
            return
        if self.split_counter > 3:
            return

        value = str(player.get_higher_value())
        if self.split_counter == 0:
            draw_card(f"        {value}", window, CARD_SPLIT_SIZE[0], CARD_SPLIT_SIZE[1],
                      player.card_split_pos)
        elif self.split_counter == 1:
            draw_card(f"        {value}", window, CARD_SPLIT_SIZE[0], CARD_SPLIT_SIZE[1],
                      (player.card_split_pos[0] + NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR, player.card_split_pos[1]))
        elif self.split_counter == 2:
            draw_card(f"        {value}", window, CARD_SPLIT_SIZE[0], CARD_SPLIT_SIZE[1],
                      (player.card_split_pos[0] + NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR +
                       NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR, player.card_split_pos[1]))
        elif self.split_counter == 3:
            draw_card(f"        {value}", window, CARD_SPLIT_SIZE[0], CARD_SPLIT_SIZE[1],
                      (player.card_split_pos[0] + NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR +
                       NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR + NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR, player.card_split_pos[1]))
        self.split_counter += 1

        pygame.time.Clock().tick(60)
        pygame.display.update()

    def check_player_win(self, dealer, player):  # return 1 if player won, 0 if it's a tie, -1 if dealer won
        if player.blackjack is True and dealer.blackjack is True:
            return 0
        if player.blackjack is True:
            return 1
        if dealer.blackjack is True:
            return -1
        if player.bust is True:
            return -1
        if dealer.bust is True:
            return 1
        if player.get_higher_value() > dealer.get_higher_value():
            return 1
        if player.get_higher_value() < dealer.get_higher_value():
            return -1
        return 0

    def update_money_according_to_win_or_loose(self, dealer, player, check_value):
        p = player.get_root_player()
        if check_value == 1:
            p.money += 2 * player.bet
            if player.blackjack is True:
                p.money += 0.5 * player.bet
                return player.bet + 0.5 * player.bet
            return player.bet
        elif check_value == 0:
            p.money += player.bet
            return 0
        else:
            dealer.money += player.bet
            return -1 * player.bet

    def checking_if_players_are_broke(self):
        remove_list = []
        for p in self.players:
            if p.money < 1:
                # print you are broke f"player {p.player_num you are broke. You have less than 1 money :("
                remove_list += [p]  # adding the player for the remove list
        self.remove_players(remove_list)
        if not self.players:
            pass
            # print game end because no players left
            # go back to the menu
            return True
        return False

    def remove_players(self, remove_list):
        for player in remove_list:
            self.players.remove(player)
            self.players_amount -= 1

    def new_round(self, window):

        print("---------- NEW ROUND ----------\n")

        # checking for a reshuffle for the decks
        if self.check_for_red_card() is True:
            self.deck.shuffle()
            self.deck.place_red_card()
            print("deck reshuffled")
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, 45, 0)
            write_text(window, TEXT_INFO_POS, "Red card was drawn. Deck reshuffled", text_font=30)
            pygame.time.Clock().tick(60)
            pygame.display.update()
            time.sleep(2)
            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, 45, 0)

        # placing bets
        if self.placing_bets(window) is False:
            return False

        # adding cards to players and dealer
        for i in range(2):
            for p in self.players:
                if i == 0:  # drawing the player info
                    if p.player_num == 1:
                        write_text(window, TEXT_PLAYER1_POS, f"player {p.player_num}")
                        write_text(window, TEXT_PLAYER1_BET_POS, f"original bet: {p.bet}")
                        write_text(window, (TEXT_PLAYER1_BET_POS[0], TEXT_PLAYER1_BET_POS[1] + 30), f"money: {p.money}")
                    elif p.player_num == 2:
                        write_text(window, TEXT_PLAYER2_POS, f"player {p.player_num}")
                        write_text(window, TEXT_PLAYER2_BET_POS, f"original bet: {p.bet}")
                        write_text(window, (TEXT_PLAYER2_BET_POS[0], TEXT_PLAYER2_BET_POS[1] + 30), f"money: {p.money}")
                    elif p.player_num == 3:
                        write_text(window, TEXT_PLAYER3_POS, f"player {p.player_num}")
                        write_text(window, TEXT_PLAYER3_BET_POS, f"original bet: {p.bet}")
                        write_text(window, (TEXT_PLAYER3_BET_POS[0], TEXT_PLAYER3_BET_POS[1] + 30), f"money: {p.money}")
                    elif p.player_num == 4:
                        write_text(window, TEXT_PLAYER4_POS, f"player {p.player_num}")
                        write_text(window, TEXT_PLAYER4_BET_POS, f"original bet: {p.bet}")
                        write_text(window, (TEXT_PLAYER4_BET_POS[0], TEXT_PLAYER4_BET_POS[1] + 30), f"money: {p.money}")
                p.add_card(self.deck.deck.pop(0), window)
                self.cards_used += 1
            self.dealer.dealer.add_card(self.deck.deck.pop(0), window)
            self.cards_used += 1
        self.dealer.up_card = self.dealer.dealer.cards[1]  # making the second card for the dealer 'up'

        write_text(window, TEXT_DEALER_POS, f"dealer")  # drawing dealer info
        pygame.time.Clock().tick(60)
        pygame.display.update()

        # printing the players cards
        for p in self.players:
            print(f"player {p.player_num} cards:", end=' ')
            print(p.cards, end=' ')
        print()

        # printing the dealer up card
        print("the dealer up cards is: " + self.dealer.up_card)

        # actions phase
        if self.action_phase(self.players, window) is False:
            return False

        # dealer action
        self.cards_used += self.dealer.dealer_action(self.deck.deck, window)  # before there was pop to card and a change in dealer: instead of deck it was card

        # determine who won and give money according to bets
        for p in self.players:
            money_win = 0
            if p.split is None:
                check_value = self.check_player_win(self.dealer.dealer, p)
                money_win += self.update_money_according_to_win_or_loose(self.dealer.dealer, p, check_value)
            else:
                p.set_sons_player_list()
                for son_player in p.sons:
                    check_value = self.check_player_win(self.dealer.dealer, son_player)
                    money_win += self.update_money_according_to_win_or_loose(self.dealer.dealer, son_player,
                                                                             check_value)
            status = ""
            if money_win > 0:
                status = " won "
            elif money_win < 0:
                status = " lost "
            else:
                status = " won no money. "
            print("player " + str(p.player_num) + status + str(money_win) + " money added to your balance")

            draw_rotated_rectangle(window, DARK_GREEN_COLOR, TEXT_INFO_POS, WIDTH, FONT_NUMBER * 2, 0)  # clear text
            write_text(window, TEXT_INFO_POS, "player " + str(p.player_num) + status + str(abs(money_win)) + " money", text_font=40)
            pygame.time.Clock().tick(60)
            pygame.display.update()
            time.sleep(2)

        # reset players and the dealer
        for p in self.players:
            p.reset_player()
        self.dealer.dealer.reset_player()

        print("---------- END ROUND ----------\n")

        if self.checking_if_players_are_broke() is True:
            return False

        return True
