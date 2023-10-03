from blackjack.player import *


class Dealer:
    def __init__(self):
        self.dealer = Player(0)
        self.up_card = ""

    def dealer_action(self, deck, window):
        self.dealer.card_pos[1] = 0
        draw_rotated_rectangle(window, DARK_GREEN_COLOR, DEALER_FIRST_POS, WIDTH, CARD_SIZE[1], 0)  # clear dealer cards
        text1 = text2 = ''
        if self.dealer.cards[0] != '10':
            text1 = self.dealer.cards[0][0]
        else:
            text1 = '10'
        if self.dealer.cards[1] != '10':
            text2 = self.dealer.cards[1][0]
        else:
            text2 = '10'
        draw_card(text1, window, CARD_SIZE[0], CARD_SIZE[1],
                  (self.dealer.card_pos[0][0] + self.dealer.card_pos[1], self.dealer.card_pos[0][1]))
        self.dealer.card_pos[1] += NEXT_CARD_ADJUSTMENT_FACTOR
        draw_card(text2, window, CARD_SIZE[0], CARD_SIZE[1],
                  (self.dealer.card_pos[0][0] + self.dealer.card_pos[1], self.dealer.card_pos[0][1]))
        self.dealer.card_pos[1] += NEXT_CARD_ADJUSTMENT_FACTOR

        # printing the sum of the cards
        self.dealer.print_sum(window, 30)

        pygame.time.Clock().tick(60)
        pygame.display.update()
        
        print("dealer's cards:", end=' ')
        print(self.dealer.cards, end=' ')
        print(f"sum: {self.dealer.get_higher_value()}")
        cards_used = 0
        while self.dealer.total_value < 17 and self.dealer.another_total_value <= 17:  # dealer hits on soft 17
            self.dealer.add_card(deck.pop(0), window)
            cards_used += 1
            print("dealer's cards after an action:", end=' ')
            print(self.dealer.cards, end=' ')
            print(f"sum: {self.dealer.get_higher_value()}")
            self.dealer.print_sum(window, 30)  # printing the sum of the cards

        return cards_used
