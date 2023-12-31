DARK_GREEN_COLOR = (0, 100, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (125, 125, 125)
GREY_HOVER = (50, 50, 50)

WIDTH = 1200
HEIGHT = 800

DEALER_FIRST_POS = (WIDTH / 2, HEIGHT / 8)

SEAT_ONE_FIRST_POS = (WIDTH / 8, HEIGHT / 1.5)
SEAT_TWO_FIRST_POS = (WIDTH / 3, HEIGHT / 1.5)
SEAT_THREE_FIRST_POS = (WIDTH / 1.5, HEIGHT / 1.5)
SEAT_FOUR_FIRST_POS = (WIDTH / 1.125, HEIGHT / 1.5)

STAND_BUTTON_POS = (WIDTH / 3.6 + 110, HEIGHT / 2)
HIT_BUTTON_POS = (WIDTH / 3.6 + 220, HEIGHT / 2)
DOUBLE_BUTTON_POS = (WIDTH / 3.6 + 330, HEIGHT / 2)
SPLIT_BUTTON_POS = (WIDTH / 3.6 + 440, HEIGHT / 2)
BUTTON_SIZE = (100, 50)
NEXT_BUTTON_ADJUSTMENT_FACTOR = 110  # maybe adding the size of the button like in a card split

ENTER_BET_POS = HIT_BUTTON_POS
RESET_BET_POS = DOUBLE_BUTTON_POS

CARD_SIZE = (50, 50 * 1.4)

CARD_SPLIT_SIZE = (CARD_SIZE[0] / 2, CARD_SIZE[1] / 2)
CARD_ONE_SPILT_POS = (SEAT_ONE_FIRST_POS[0], HEIGHT / 1.05)
CARD_TWO_SPILT_POS = (SEAT_TWO_FIRST_POS[0], HEIGHT / 1.05)
CARD_THREE_SPILT_POS = (SEAT_THREE_FIRST_POS[0], HEIGHT / 1.05)
CARD_FOUR_SPILT_POS = (SEAT_FOUR_FIRST_POS[0], HEIGHT / 1.05)
NEXT_CARD_SPLIT_ADJUSTMENT_FACTOR = CARD_SPLIT_SIZE[0] + 10

FONT_NUMBER = 24
NEXT_CARD_ADJUSTMENT_FACTOR = FONT_NUMBER - 4  # example: ((WIDTH / 3) + 20, HEIGHT / 1.5))

TEXT_INFO_POS = (WIDTH / 2, HEIGHT / 2.5)
TEXT_PLAYER1_POS = (WIDTH / 8, HEIGHT / 1.5 + 50 * 1.4)
TEXT_PLAYER1_BET_POS = (WIDTH / 8, HEIGHT / 1.5 + 50 * 1.4 + 30)
TEXT_PLAYER2_POS = (WIDTH / 3, HEIGHT / 1.5 + 50 * 1.4)
TEXT_PLAYER2_BET_POS = (WIDTH / 3, HEIGHT / 1.5 + 50 * 1.4 + 30)
TEXT_PLAYER3_POS = (WIDTH / 1.5, HEIGHT / 1.5 + 50 * 1.4)
TEXT_PLAYER3_BET_POS = (WIDTH / 1.5, HEIGHT / 1.5 + 50 * 1.4 + 30)
TEXT_PLAYER4_POS = (WIDTH / 1.125, HEIGHT / 1.5 + 50 * 1.4)
TEXT_PLAYER4_BET_POS = (WIDTH / 1.125, HEIGHT / 1.5 + 50 * 1.4 + 30)
TEXT_DEALER_POS = (WIDTH / 2, HEIGHT / 8 + 50 * 1.4)
