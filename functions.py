import pygame
import random

# ESSENTIALS #

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1080

MAIN_FONT = pygame.font.SysFont('calibri', int(WINDOW_HEIGHT / 16), True)
MAIN_FONT_SMALL = pygame.font.SysFont('calibri', int(WINDOW_HEIGHT / 32), italic=True)


# VARIABLES #

relative_height = 0

platform_minimum_width = 250
platform_maximum_width = 400
platform_height = 25

class Platform:
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def generate_platform(id):
    return Platform(
        id,
        random.randint(platform_maximum_width / 2, WINDOW_WIDTH - platform_maximum_width / 2),
        WINDOW_HEIGHT / 4 + id * (WINDOW_HEIGHT / 2),
        random.randint(platform_minimum_width, platform_maximum_width),
        platform_height
    )

def player_rectangle(x, y, width, height):
    global relative_height
    return pygame.Rect(x - width / 2, WINDOW_HEIGHT - y - height / 2 + relative_height, width, height)

def platform_rectangle(platform):
    global relative_height
    return pygame.Rect(platform.x - platform.width / 2, WINDOW_HEIGHT - platform.y - platform.height / 2 + relative_height, platform.width, platform.height)

def draw_rectangle(window, color, rect):
    pygame.draw.rect(window, color, rect)

def draw_platform(window, rect):
    draw_rectangle(window, (255, 255, 255), rect)

def draw_score(window, score):
    text = MAIN_FONT.render(str(score), True, (24, 158, 199))
    window.blit(text, text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)))

def draw_death_message(window, score):
    text = MAIN_FONT_SMALL.render("you died, your final score is " + str(score), True, (24, 158, 199))
    text2 = MAIN_FONT_SMALL.render("press right mouse button to reset", True, (24, 158, 199))
    window.blit(text, text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - MAIN_FONT_SMALL.size("you died, your final score is ")[1] / 2)))
    window.blit(text2, text2.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + MAIN_FONT_SMALL.size("press right mouse button to reset")[1] / 2)))

def horizontal_bounce(player_velocity_x):
    player_velocity_x += (player_velocity_x / 2) * (-1)
    player_velocity_x *= -1
    return player_velocity_x

def vertical_bounce(player_velocity_x, player_velocity_y):
    player_velocity_x += (player_velocity_x / 2) * (-1)
    player_velocity_y -= player_velocity_y / 2
    player_velocity_y *= -1
    return player_velocity_x, player_velocity_y

def determine_side(rect1, rect2):
    if rect2.right > rect1.left and rect2.left < rect1.right:
        if rect2.bottom < rect1.center[1]:
            return "vertical", "top"
        else:
            return "vertical", "bottom"
    else:
        return "horizontal"

def change_relative_height(height):
    global relative_height
    if height == 'reset':
        relative_height = 0
    else:
        relative_height += height
    return relative_height