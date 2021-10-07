import pygame
import scene
import utils

from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

class SceneEditor (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.spritesheet = utils.SpriteSheet("assets/colored_packed.png", 16, 16)
        self.x = 0
        self.y = 0
        self.invalid = True
        self.images = {}

    def on_event(self, event):
        if event.type == KEYDOWN:
            self.x = self.x + (1 if event.key == K_RIGHT else 0) - (1 if event.key == K_LEFT else 0)
            self.y = self.y + (1 if event.key == K_DOWN else 0) - (1 if event.key == K_UP else 0)
            self.invalid = True

    def on_display(self, screen):
        screen.fill((0,0,0))
        if self.invalid:
            for i in range(self.x, self.x+4):
                for j in range(self.y, self.y+4):
                    self.images[i-self.x, j-self.y] = self.spritesheet.img_at(i, j, 5)
            self.invalid = False
        block = self.images[0,0].get_rect().w
        for i in range(4):
            for j in range(4):
                screen.blit(self.images[i, j], (i*block, j*block))
        font = pygame.font.SysFont("Arial", 24)
        render = font.render("({},{})".format(self.x, self.y), True, (255, 255, 255))
        screen.blit(render, (screen.get_rect().w - render.get_rect().w, 10))



    def on_update(self):
        pass

