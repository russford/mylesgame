import pygame
import scene
import scene_fight
import utils

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

        for pos, m in self.director.monsters.items():
            if m.hp > 0:
                pygame.draw.rect(screen, (0, 255, 0), self.map_rect(*pos))

        if self.detail_panel:
            blitter = utils.TextBlit ("Arial", 12, (200, 200, 200), 2)
            screen.blit (blitter(self.director.player.mirror()), self.map_rect(*self.director.player.pos))
            for pos, m in self.director.monsters.items():
                screen.blit(blitter(m.mirror()), self.map_rect(*pos))


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
            if self.director.player.pos == pos and m.hp > 0:
                fight = scene_fight.SceneFight(self.director, m)
                fight.next = self
                self.director.set_scene(fight)

    def map_rect (self, i, j):
        return pygame.Rect(i*self.block, j*self.block, self.block, self.block)

    def move (self, dir_x, dir_y):
        if (self.p_x + dir_x, self.p_y + dir_y) in self.monsters:
            pass

        if not self.map_dict[(self.p_x+dir_x, self.p_y+dir_y)]:
            self.p_x += dir_x
            self.p_y += dir_y

