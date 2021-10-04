import pygame
import random
import math

# ESSENTIALS #

pygame.init()

WINDOW = pygame.display.set_mode(flags=pygame.FULLSCREEN)
pygame.display.set_caption("Bouncy Square")
icon = pygame.image.load("assets/images/icon.ico").convert()
pygame.display.set_icon(icon)

COLLISION_SOUND = pygame.mixer.Sound("assets/sounds/collision.wav")

WINDOW_SIZE = pygame.display.get_window_size()
WINDOW_WIDTH = WINDOW_SIZE[0]
WINDOW_HEIGHT = WINDOW_SIZE[1]

PLAYAREA_WIDTH = 1000
PLAYAREA_HEIGHT = WINDOW_HEIGHT

CENTERING_OFFSET = WINDOW_WIDTH / 2 - PLAYAREA_WIDTH / 2

MAIN_FONT = pygame.font.SysFont('calibri', int(PLAYAREA_HEIGHT / 16), True)
MAIN_FONT_SMALL = pygame.font.SysFont('calibri', int(PLAYAREA_HEIGHT / 32), italic=True)

# VARIABLES #

relative_height = 0

platform_minimum_width = 300
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
        random.randint(platform_maximum_width / 2, PLAYAREA_WIDTH - platform_maximum_width / 2),
        PLAYAREA_HEIGHT / 4 + id * (PLAYAREA_HEIGHT / 2),
        random.randint(platform_minimum_width, platform_maximum_width),
        platform_height
    )

def player_rectangle(x, y, width, height):
    global relative_height
    return pygame.Rect(CENTERING_OFFSET + x - width / 2, PLAYAREA_HEIGHT - y - height / 2 + relative_height, width, height)

def platform_rectangle(platform):
    global relative_height
    return pygame.Rect(CENTERING_OFFSET + platform.x - platform.width / 2, PLAYAREA_HEIGHT - platform.y - platform.height / 2 + relative_height, platform.width, platform.height)

def draw_rectangle(color, rect):
    pygame.draw.rect(WINDOW, color, rect)

def draw_walls():
    pygame.draw.rect(WINDOW, (255, 255, 255), pygame.Rect(WINDOW_WIDTH / 2 - PLAYAREA_WIDTH / 2 - platform_height, 0, platform_height, WINDOW_HEIGHT))
    pygame.draw.rect(WINDOW, (255, 255, 255), pygame.Rect(WINDOW_WIDTH / 2 + PLAYAREA_WIDTH / 2, 0, platform_height, WINDOW_HEIGHT))

def draw_platform(rect):
    draw_rectangle((255, 255, 255), rect)

def draw_score(score):
    text = MAIN_FONT.render(str(score), True, (24, 158, 199))
    WINDOW.blit(text, text.get_rect(center=(CENTERING_OFFSET + PLAYAREA_WIDTH / 2, PLAYAREA_HEIGHT / 2)))

def draw_death_message(score):
    text = MAIN_FONT_SMALL.render("you died, your final score is " + str(score), True, (24, 158, 199))
    text2 = MAIN_FONT_SMALL.render("press right mouse button to reset", True, (24, 158, 199))
    WINDOW.blit(text, text.get_rect(center=(CENTERING_OFFSET + PLAYAREA_WIDTH / 2, PLAYAREA_HEIGHT / 2 - MAIN_FONT_SMALL.size("you died, your final score is ")[1] / 2)))
    WINDOW.blit(text2, text2.get_rect(center=(CENTERING_OFFSET + PLAYAREA_WIDTH / 2, PLAYAREA_HEIGHT / 2 + MAIN_FONT_SMALL.size("press right mouse button to reset")[1] / 2)))

def draw_fps(frame_time):
    text = MAIN_FONT_SMALL.render(str(math.floor(frame_time)), True, (255, 255, 255))
    WINDOW.blit(text, text.get_rect())

def draw_clicked_point(mouse_start_position):
    pygame.draw.circle(WINDOW, (92, 92, 92), (mouse_start_position[0], mouse_start_position[1]), 5)

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

def change_difficulty(score):
    global platform_minimum_width
    global platform_maximum_width
    if score == "reset":
        platform_minimum_width = 250
        platform_maximum_width = 400
    elif score % 10 == 0 and score < 500:
        platform_minimum_width -= 28
        platform_maximum_width -= 34

def play_collision_sound():
    pygame.mixer.Sound.play(COLLISION_SOUND)