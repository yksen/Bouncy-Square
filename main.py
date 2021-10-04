from functions import *
import pygame
import pygame.constants
import sys

# ESSENTIALS #

pygame.init()

FRAME_TIME = pygame.time.Clock()

# VARIABLES #

show_fps = False

dt = 0.001
gravity = -10

collision_occured = False
screen_scrolling_active = False
relative_height = 0
height_increase = 3

player_x = 500
player_y = 100
player_width = 50
player_height = player_width
player_velocity_x = 0
player_velocity_y = 0

mouse_clicked = False
mouse_start_position = (0, 0)
mouse_end_position = (0, 0)

score = 0
player_alive = True
death_enabled = False

platform_id = 0
platforms = []
platforms.append(generate_platform(platform_id))
platform_id += 1
platforms.append(generate_platform(platform_id))

# GAME LOOP #

while True:

    # EVENTS #
    
    events = pygame.event.get()
    for event in events:        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not mouse_clicked and player_alive:
            mouse_clicked = True
            mouse_start_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_clicked and player_alive:
            mouse_clicked = False
            mouse_end_position = pygame.mouse.get_pos()
            player_velocity_x += (mouse_start_position[0] - mouse_end_position[0]) * 0.015
            player_velocity_y -= (mouse_start_position[1] - mouse_end_position[1]) * 0.015
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_clicked = False
            screen_scrolling_active = False
            relative_height = change_relative_height("reset")
            height_increase = 1
            
            player_x = 500
            player_y = 100
            player_velocity_x = 0
            player_velocity_y = 0
            platforms.clear()
            score = 0
            player_alive = True
            death_enabled = False

            change_difficulty("reset")

            platform_id = 0
            platforms = []
            platforms.append(generate_platform(platform_id))
            platform_id += 1
            platforms.append(generate_platform(platform_id))
        if event.type == pygame.KEYUP and event.key == pygame.K_v:
            show_fps = True
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.constants.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # DRAWING #

    WINDOW.fill((0, 0, 0))
    draw_walls()

    if screen_scrolling_active and relative_height < (PLAYAREA_HEIGHT / 2) * (platform_id - 1):        
        relative_height = change_relative_height(dt * 1000 * height_increase)
        if relative_height + height_increase >= (PLAYAREA_HEIGHT / 2) * (platform_id - 1):
            screen_scrolling_active = False

    if player_alive:
        draw_score(score)
    else:
        draw_death_message(score)

    draw_rectangle((150, 27, 95), player_rectangle(player_x, player_y, player_width, player_height))
    for platform in platforms:
        draw_platform(platform_rectangle(platform))

    if mouse_clicked:
        draw_clicked_point(mouse_start_position)

    if show_fps:
        draw_fps(FRAME_TIME.get_fps())

    pygame.display.update()

    # COLLISIONS #
    collision_occured = False
    if player_x + player_velocity_x < player_width / 2 or player_x + player_velocity_x > PLAYAREA_WIDTH - player_width / 2:
        player_velocity_x = horizontal_bounce(player_velocity_x)
        collision_occured = True
    if player_y + player_velocity_y < player_height / 2 + relative_height:
        if death_enabled:
            player_alive = False
        else:
            player_velocity_x, player_velocity_y = vertical_bounce(player_velocity_x, player_velocity_y)
            collision_occured = True
    elif player_y + player_velocity_y > PLAYAREA_HEIGHT - player_height / 2 + relative_height:
        player_velocity_x, player_velocity_y = vertical_bounce(player_velocity_x, player_velocity_y)
        collision_occured = True
    for platform in platforms:
        player_rect = player_rectangle(player_x + player_velocity_x, player_y + player_velocity_y, player_width, player_height)
        platform_rect = platform_rectangle(platform)
        if pygame.Rect.colliderect(player_rect, platform_rect):
            collision_occured = True
            player_rect = player_rectangle(player_x, player_y, player_width, player_height)
            collision_side = determine_side(platform_rect, player_rect)
            if collision_side[0] == "vertical":
                player_velocity_x, player_velocity_y = vertical_bounce(player_velocity_x, player_velocity_y)
                if collision_side[1] == "top" and platform.id + 1 > score:
                    score = platform.id + 1
            else:
                player_velocity_x = horizontal_bounce(player_velocity_x)

    if collision_occured and player_velocity_y > 0.1:
        play_collision_sound()

    # PHYSICS #

    player_x += player_velocity_x
    player_y += player_velocity_y
    player_velocity_y += gravity * dt

    # GAME #
    
    if score == platform_id + 1:
        change_difficulty(score)
        if score == 2:
            death_enabled = True
        platform_id += 1
        platforms.append(generate_platform(platform_id))
        screen_scrolling_active = True
        platforms.pop(0)

    # TIME #
    
    FRAME_TIME.tick()
    dt = 0.001 * FRAME_TIME.get_time()