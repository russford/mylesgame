# Import the pygame module
import pygame
import pygame.freetype
import game_map

# Import random for random numbers
import random


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_BACKSPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep our main loop running
running = True

clockobject = pygame.time.Clock()

# Our main loop
active_text = ""
strings = []

game = game_map.GameMap ("map2.txt")


while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP:
                game.move(0,-1)
            elif event.key == K_DOWN:
                game.move(0,1)
            elif event.key == K_LEFT:
                game.move(-1, 0)
            elif event.key == K_RIGHT:
                game.move(1, 0)
            elif event.key == K_RETURN:
                if active_text:
                    strings.append(active_text)
                    active_text = ""
            elif event.key == K_BACKSPACE:
                active_text = active_text[:-1]
            else:
                active_text += event.unicode

        elif event.type == QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    font = pygame.freetype.Font(None, 20)
    y = 0
    for str in ["player at ({}, {})".format(game.p_x, game.p_y)] + strings + [active_text]:
        img = font.render_to (screen, (screen.get_rect().w * 2 // 3+10, y+20), str, (255,255,255))
        y += img.h + 5


    map_screen = pygame.Surface( (screen.get_rect().w * 2 // 3 - 20, screen.get_rect().h - 20 ))
    game.render(map_screen)
    screen.blit(map_screen, (10,10))






    # Flip everything to the display
    clockobject.tick(60)
    pygame.display.flip()