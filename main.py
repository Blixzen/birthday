import pygame
import random
import string

pygame.init()

random.seed(42)

CELL_SIZE = 19
GRID_WIDTH = 26  # ~130mm width
GRID_HEIGHT = 26  # ~130mm height
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption('Mask')

font = pygame.font.SysFont('couriernew', 20)  # Monospace font
letters = string.ascii_letters.lower()

# Calculate offsets once
sample_letter = font.render('m', True, (0, 0, 0))  # Use 'm' as reference
letter_width = sample_letter.get_width()
letter_height = sample_letter.get_height()
x_offset = (CELL_SIZE - letter_width) // 2
y_offset = (CELL_SIZE - letter_height) // 2

letter_positions = []
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = (col * CELL_SIZE) + x_offset
        y = (row * CELL_SIZE) + y_offset
        letter = random.choice(letters)
        letter_positions.append((x, y, letter))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for x, y, letter in letter_positions:
        text_surface = font.render(letter, True, (0, 0, 0))
        screen.blit(text_surface, (x, y))

    pygame.display.flip()

pygame.quit()