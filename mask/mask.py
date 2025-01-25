import pygame
import random
import string
from rich.console import Console
import subprocess
import os

console = Console()

pygame.init()

random.seed(42)

img = pygame.image.load('mask/image.png')
img_window = pygame.display.set_mode((img.get_width(), img.get_height()), pygame.NOFRAME)
img_window.blit(img, (0, 0))
pygame.display.flip()

img_x, img_y = 100, 100
dragging = False
drag_offset_x = 0
drag_offset_y = 0

CELL_SIZE = 19
GRID_WIDTH = 26  # ~130mm width
GRID_HEIGHT = 26  # ~130mm height
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption('Mask')

font = pygame.font.SysFont('couriernew', 20)  # Monospace font
input_font = pygame.font.SysFont('couriernew', 24)  # Monospace font
letters = string.ascii_letters

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

input_text = ''
input_box_rect = pygame.Rect(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40)

def solved():
    console.print('[green]Пароль верный![/green]')
    console.print('[green]Перенаправляем вас дальше![/green]')
    subprocess.run(['python', 'main.py'])
    pygame.quit()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(f'Input text: {input_text}')
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
            if input_text == 'quit':
                running = False
                solved()
            elif input_text == 'finished':
                subprocess.run(['notepad.exe', 'WON.txt'])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if mouse_x > img_x and mouse_x < img_x + img.get_width() and \
                   mouse_y > img_y and mouse_y < img_y + img.get_height():
                    dragging = True
                    drag_offset_x = mouse_x - img_x
                    drag_offset_y = mouse_y - img_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                img_x = mouse_x - drag_offset_x
                img_y = mouse_y - drag_offset_y

    screen.fill((255, 255, 255))

    img_window.blit(img, (img_x, img_y))

    for x, y, letter in letter_positions:
        text_surface = font.render(letter, True, (0, 0, 0))
        screen.blit(text_surface, (x, y))

    pygame.draw.rect(screen, (200, 200, 200), input_box_rect)
    input_surface = input_font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (10, WINDOW_HEIGHT - 30))

    pygame.display.flip()


pygame.quit()