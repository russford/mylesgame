import pygame

from pygame.locals import (
    K_BACKSPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN
)

class TextBlock (object):
    def __init__ (self):
        self.strings = []
        self.active_text = ""

    def process (self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.strings.append (self.active_text)
                return 1
            elif event.key == K_ESCAPE:
                self.active_text = ""
            elif event.key == K_BACKSPACE:
                self.active_text = self.active_text[:-1]
            else:
                self.active_text += event.unicode
        return 0

    def display (self, surface):
        font = pygame.freetype.Font(None, 20)
        y = 0
        for string in self.strings + [self.active_text]:
            img = font.render_to(surface, (0, y), string, (255, 255, 255))
            y += img.h + 5

    def print (self, string):
        self.strings.append(string)

    def get_input(self, surface, screen, x, y):
        self.active_text = ""
        while True:
            for event in pygame.event.get():
                if self.process (event):
                    return_str = self.active_text[:]
                    self.active_text = ""
                    return return_str
            self.display(surface)
            screen.blit (surface, (x, y))
            pygame.display.flip()




