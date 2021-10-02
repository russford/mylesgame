# Import the pygame module
import pygame
import pygame.freetype
import scene_map
import textblock

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
    K_TAB,
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

pygame.freetype.init()
game = scene_map.GameMap ("map2.txt")
text = textblock.TextBlock()
text.print ("this is line 1")
text.print ("this is line 2")

text_screen = pygame.Surface ( (screen.get_rect().w // 3 - 20, screen.get_rect().h - 20 ))
while running:
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
            if game.state == scene_map.STATE_MOVE:
                if event.key == K_UP:
                    game.move(0,-1)
                elif event.key == K_DOWN:
                    game.move(0,1)
                elif event.key == K_LEFT:
                    game.move(-1, 0)
                elif event.key == K_RIGHT:
                    game.move(1, 0)
                elif event.key == K_TAB:
                    line = text.get_input(text_screen, screen, screen.get_rect().w * 2 // 3 - 20, 10)
                    print ("got line {}".format(line))

        elif event.type == QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    map_screen = pygame.Surface( (screen.get_rect().w * 2 // 3 - 20, screen.get_rect().h - 20 ))
    game.render(map_screen)
    screen.blit(map_screen, (10,10))

    text_screen = pygame.Surface ( (screen.get_rect().w // 3 - 20, screen.get_rect().h - 20 ))
    text.display(text_screen)
    screen.blit (text_screen, (screen.get_rect().w * 2 // 3 - 20, 10))


    # Flip everything to the display
    clockobject.tick(60)
    pygame.display.flip()