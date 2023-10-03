import pygame

from blackjack.constants import BLACK


def draw_rotated_rectangle(screen, color, center, width, height, angle):
    rectangle_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(rectangle_surface, color, (0, 0, width, height))
    rotated_rectangle = pygame.transform.rotate(rectangle_surface, angle)
    rotated_rect_center = rotated_rectangle.get_rect(center=center)
    screen.blit(rotated_rectangle, rotated_rect_center)


def write_text(window, center, text, text_font=24):
    font = pygame.font.Font(None, text_font)
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=center)
    window.blit(text, text_rect)


def draw_button(screen, color, center, width, height, text):
    top_left_x = center[0] - width / 2
    top_left_y = center[1] - height / 2

    outline_rect = pygame.Rect(top_left_x, top_left_y, width, height)
    draw_rotated_rectangle(screen, color, center, width, height, 0)

    pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2)  # rect outline

    write_text(screen, center, text)


# Function to draw a card with a number/face
def draw_card(card_value, window, width, height, rect_center):
    # Font for drawing card numbers/faces
    font = pygame.font.Font(None, 24)

    top_left_x = rect_center[0] - width / 2
    top_left_y = rect_center[1] - height / 2

    # Draw the card rectangle
    card_rect = pygame.Rect(top_left_x, top_left_y, width, height)
    pygame.draw.rect(window, (255, 255, 255), card_rect)  # rect with number
    pygame.draw.rect(window, (0, 0, 0), card_rect, 2)  # rect outline

    # Draw the card value (number/face)
    text = font.render(str(card_value), True, BLACK)
    text_rect = text.get_rect(center=(card_rect.centerx - 16, card_rect.centery - 24))
    window.blit(text, text_rect)
