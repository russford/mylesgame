import pygame
import scene
import utils

from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    MOUSEBUTTONDOWN
)

# class SelectorPanel(object):
#     def __init__(self, spritesheet, blocksize):
#         self.x, self.y = 0, 0
#         self.spritesheet = spritesheet
#         self.blocksize = blocksize
#         self.sel_x, self.sel_y = 0, 0
#         self.rect = pygame.rect.Rect(0, 0, 2*blocksize, 12*blocksize)
#         self.surface = pygame.surface.Surface
#         self.load_sprites()
#
#     def on_click (self, pos):
#         tile =
#
#
#     def on_press (self, key):
#         self.x = self.x + (1 if event.key == K_RIGHT else 0) - (1 if event.key == K_LEFT else 0)
#         self.y = self.y + (1 if event.key == K_DOWN else 0) - (1 if event.key == K_UP else 0)
#
#     def on_draw (self, screen):
#         pass
#
#     def load_sprites(self):
#         self.sprites = pygame.sprite.Group()
#         for i in range(2):
#             for j in range(12):
#                 s = Sprite()



class SceneEditor (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.spritesheet = utils.SpriteSheet("assets/colored_packed.png", 16, 16)
        self.x, self.y = 0, 0
        self.map_x, self.map_y = 0, 0
        self.invalid = True
        self.images = {}
        self.map_dict = {}
        self.active_panel = 1
        self.selector_rect = pygame.rect.Rect(0, 2*)

    def on_event(self, event):
        if event.type == KEYDOWN:
            self.x = self.x + (1 if event.key == K_RIGHT else 0) - (1 if event.key == K_LEFT else 0)
            self.y = self.y + (1 if event.key == K_DOWN else 0) - (1 if event.key == K_UP else 0)
            self.invalid = True
        if event.type == MOUSEBUTTONDOWN:


    def on_display(self, screen):
        screen.fill((0,0,0))
        if self.invalid:
            for i in range(self.x, self.x+2):
                for j in range(self.y, self.y+12):
                    self.images[i-self.x, j-self.y] = self.spritesheet.img_at(i, j, 32)
            self.invalid = False
        block = self.images[0,0].get_rect().w
        for i in range(2):
            for j in range(10):
                screen.blit(self.images[i, j], (i*block, j*block))
        font = pygame.font.SysFont("Arial", 24)
        render = font.render("({},{})".format(self.x, self.y), True, (255, 255, 255))
        screen.blit(render, (screen.get_rect().w - render.get_rect().w, 10))



    def on_update(self):
        pass

