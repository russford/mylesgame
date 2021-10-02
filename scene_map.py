import pygame
from collections import defaultdict
import scene
import scene_fight

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    MOUSEBUTTONDOWN
)

move_dict = {K_UP: (0,-1), K_DOWN: (0,1), K_LEFT: (-1,0), K_RIGHT: (1,0)}


class SceneMap (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.block = 0
        self.detail_panel = False

    def on_display(self, screen):
        screen.fill((0,0,0))

        self.block = min(screen.get_rect().w // self.director.map_w, screen.get_rect().h // self.director.map_h)

        for i in range(self.director.map_w):
            for j in range(self.director.map_h):
                if (i,j) in self.director.map_dict:
                    pygame.draw.rect(screen, (128, 128, 128), self.map_rect(i, j))

        pygame.draw.rect(screen, (255, 0, 0), self.map_rect(*self.director.player.pos))

        for mx, my in self.director.monsters.keys():
            pygame.draw.rect(screen, (0, 255, 0), self.map_rect(mx, my))

        if self.detail_panel:
            panel = self.build_details(self.director.player)
            screen.blit (panel, self.map_rect(*self.director.player.pos))
            for pos, m in self.director.monsters.items():
                panel = self.build_details(m)
                screen.blit(panel, self.map_rect(*pos))

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key in move_dict.keys():
                direction = move_dict[event.key]
                new_pos = self.director.player.pos[0] + direction[0], self.director.player.pos[1] + direction[1]
                if new_pos not in self.director.map_dict:
                    self.director.player.pos = new_pos
            elif event.key == K_SPACE:
                self.detail_panel = True
        elif event.type == KEYUP and event.key == K_SPACE:
            self.detail_panel = False

    def on_update(self):
        for pos, m in self.director.monsters.items():
            if self.director.player.pos == pos:
                fight = scene_fight.SceneFight(self.director, m)
                fight.prev = self
                self.director.set_scene(fight)

    def build_details (self, player):
        font = pygame.font.SysFont ("Calibri", 10)
        renders = [font.render(s, 1, (200,200,200)) for s in player.mirror()]
        rects = [r.get_rect() for r in renders]
        h = sum([r.h for r in rects]) + (len(rects)-1) * 2
        w = max([r.w for r in rects])
        surf = pygame.surface.Surface((w, h))
        for i in range(len(renders)):
            surf.blit(renders[i], (0, 12*i))
        return surf


    def map_rect (self, i, j):
        return pygame.Rect(i*self.block, j*self.block, self.block, self.block)

    # def render (self, surface):
    #     self.block_size = min(surface.get_rect().w // self.map_size[0], surface.get_rect().h // self.map_size[1])
    #     for i in range(self.map_size[0]):
    #         for j in range(self.map_size[1]):
    #             if self.map_dict[(i,j)]:
    #                 pygame.draw.rect (surface, (128, 128, 128), self.map_rect(i, j))
    #     pygame.draw.rect (surface, (255,0,0), self.map_rect(self.p_x, self.p_y))
    #     for mx, my in self.monsters:
    #         pygame.draw.rect (surface, (0,255,0), self.map_rect (mx, my))


    def move (self, dir_x, dir_y):
        if (self.p_x + dir_x, self.p_y + dir_y) in self.monsters:
            pass

        if not self.map_dict[(self.p_x+dir_x, self.p_y+dir_y)]:
            self.p_x += dir_x
            self.p_y += dir_y

