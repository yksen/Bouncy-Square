import pygame

def draw_centered_rectangle(x, y, width, height, color, window):
    pygame.draw.rect(window, color, pygame.Rect(x - width / 2, y - height / 2, width, height))

