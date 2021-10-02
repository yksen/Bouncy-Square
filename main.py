from functions import *
import pygame
import pygame.constants
import random
import sys

# ESSENTIALS #

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game2")

MAIN_FONT =  pygame.font.SysFont('calibri', 24)

FRAME_TIME = pygame.time.Clock()

# VARIABLES #

dt = 0.001
gravity = 10

player_x = 500
player_y = 500
player_width = 100
player_height = player_width
player_velocity_x = 0
player_velocity_y = 0

mouse_clicked = False
mouse_start_position = (0, 0)
mouse_end_position = (0, 0)

# GAME LOOP #

while True:

    # EVENTS #
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not mouse_clicked:
            mouse_clicked = True
            mouse_start_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_clicked:
            mouse_clicked = False
            mouse_end_position = pygame.mouse.get_pos()
            player_velocity_x += (mouse_start_position[0] - mouse_end_position[0]) * 0.01
            player_velocity_y += (mouse_start_position[1] - mouse_end_position[1]) * 0.01

    # DRAWING #

    WINDOW.fill((0, 0, 0))
    draw_centered_rectangle(player_x, player_y, player_width, player_height, (150, 27, 95), WINDOW)
    pygame.display.update()

    # PHYSICS #

    player_x += player_velocity_x
    player_y += player_velocity_y

    player_velocity_y += gravity * dt

    if player_x + player_velocity_x < player_width / 2 or player_x + player_velocity_x > WINDOW_WIDTH - player_width / 2:
        player_velocity_x += (player_velocity_x / 2) * (-1)
        player_velocity_x *= -1
    if player_y + player_velocity_y < player_height / 2 or player_y + player_velocity_y > WINDOW_HEIGHT - player_height / 2:
        player_velocity_x += (player_velocity_x / 2) * (-1)
        player_velocity_y -= player_velocity_y / 2
        player_velocity_y *= -1
    
    # TIME #

    FRAME_TIME.tick()
    dt = 0.001 * FRAME_TIME.get_time()