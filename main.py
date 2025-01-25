import pygame
import subprocess
import random
import time

pygame.init()

screen = pygame.display.set_mode([1280, 720])

player_forward = pygame.image.load('assets/mine/bob_forward.png')
player_left = pygame.image.load('assets/mine/bob_left.png')
player_right = pygame.image.load('assets/mine/bob_right.png')
player_backward = pygame.image.load('assets/mine/bob_backward.png')

player_forward = pygame.transform.scale(player_forward, (64, 64))
player_left = pygame.transform.scale(player_left, (64, 64))
player_right = pygame.transform.scale(player_right, (64, 64))
player_backward = pygame.transform.scale(player_backward, (64, 64))

player_image = player_forward

player_x = 640
player_y = 360
player_speed = 1.3

class Enemy:
    def __init__(self):
        self.image = pygame.image.load('assets/mine/enemy.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.spawn_position()

    def spawn_position(self):
        edge = random.choice(['left', 'right', 'top', 'bottom'])
        if edge == 'left':
            self.rect.x = -64
            self.rect.y = random.randint(0, 720)
            self.speed_x = random.uniform(1, 3)
            self.speed_y = 0
        elif edge == 'right':
            self.rect.x = 1280
            self.rect.y = random.randint(0, 720)
            self.speed_x = -random.uniform(1, 3)
            self.speed_y = 0
        elif edge == 'top':
            self.rect.x = random.randint(0, 1280)
            self.rect.y = -64
            self.speed_x = 0
            self.speed_y = random.uniform(1, 3)
        elif edge == 'bottom':
            self.rect.x = random.randint(0, 1280)
            self.rect.y = 720
            self.speed_x = 0
            self.speed_y = -random.uniform(1, 3)
        print(f"Enemy spawned at ({self.rect.x}, {self.rect.y}) moving with speed ({self.speed_x}, {self.speed_y})")

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

enemies = []

spawn_rate = 1000
last_spawn_time = pygame.time.get_ticks()

font = pygame.font.Font(None, 36)

total_game_time = 16
start_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= player_speed
        player_image = player_left
    if keys[pygame.K_d]:
        player_x += player_speed
        player_image = player_right
    if keys[pygame.K_w]:
        player_y -= player_speed
        player_image = player_forward
    if keys[pygame.K_s]:
        player_y += player_speed
        player_image = player_backward

    if player_x < 0:
        player_x = 0
    if player_x > 1280 - 64:
        player_x = 1280 - 64
    if player_y < 0:
        player_y = 0
    if player_y > 720 - 64:
        player_y = 720 - 64

    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_rate:
        enemies.append(Enemy())
        last_spawn_time = current_time
        spawn_rate = max(100, spawn_rate - 50)
        print(f"Spawned enemy at {current_time}, new spawn rate: {spawn_rate}")

    for enemy in enemies:
        enemy.move()

    player_rect = pygame.Rect(player_x, player_y, 64, 64)
    for enemy in enemies:
        if player_rect.colliderect(enemy.rect):
            running = False

    screen.fill((255, 255, 255))
    screen.blit(player_image, (player_x, player_y))

    for enemy in enemies:
        screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

    spawn_rate_text = font.render(f'Spawn Rate: {spawn_rate} ms', True, (0, 0, 0))
    screen.blit(spawn_rate_text, (10, 10))

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, total_game_time - elapsed_time)
    time_left_text = font.render(f'Time Left: {time_left:.2f} s', True, (0, 0, 0))
    screen.blit(time_left_text, (10, 40))

    if time_left <= 0:
        win_text = font.render('You Win!', True, (0, 0, 0))
        screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 2 - win_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        subprocess.run(['notepad.exe', 'yay.txt'])
        running = False
        exit()

    pygame.display.flip()

pygame.quit()