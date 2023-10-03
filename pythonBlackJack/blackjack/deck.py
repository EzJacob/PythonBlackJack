import os
import random
import math
import pygame

CARDS_AMOUNT_IN_DECK = 52
DECK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4


class Deck:
    def __init__(self, amount_of_decks):
        self.amount_of_decks = amount_of_decks
        self.deck = self.shuffle()
        self.red_card_index = self.place_red_card()

    def shuffle(self):

        # play sound
        # Get the current directory (folder 'a' in this case)
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Define the path to folder 'b'
        folder_sounds_path = os.path.join(os.path.dirname(current_directory), 'sounds')

        # Now, you can access files in folder 'b' using folder_b_path
        file_in_sounds_path = os.path.join(folder_sounds_path, 'shuffling_cards_sound.wav')

        # playing the sound
        shuffle_cards_sound = pygame.mixer.Sound(file_in_sounds_path)
        shuffle_cards_sound.set_volume(0.4)
        shuffle_cards_sound.play()

        deck = DECK * self.amount_of_decks
        random.shuffle(deck)
        return deck

    def shuffle_without_cards_used(self, list_cards):
        self.deck = self.shuffle()
        for card in list_cards:
            self.deck.remove(card)
        self.red_card_index = self.place_red_card()

    # after 70% to 80% of cards used reshuffle the deck
    def place_red_card(self):
        percentage = random.randint(70, 80)
        sum_of_cards = len(self.deck)
        red_card_index = math.ceil((percentage * sum_of_cards) / 100)
        return red_card_index
