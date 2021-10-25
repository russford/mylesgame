import pygame
import scene
import scene_fight
import utils

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    MOUSEBUTTONDOWN
)

move_dict = {K_UP: (0,-1), K_DOWN: (0,1), K_LEFT: (-1,0), K_RIGHT: (1,0)}


class SceneMap (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.map_x, self.map_y = 0, 0
        self.block = 24
        self.spritesheet = utils.SpriteSheet("assets/colored_packed.png", 16, 16)

    def on_display(self, screen):
        screen.fill((0, 0, 0))

        all_players = self.director.monsters | {self.director.player.pos: self.director.player}
        for i in range(self.block):
            for j in range(self.block):
                block_spot = (i + self.map_x, j + self.map_y)
                if block_spot in self.director.worldmap.map_dict:
                    screen.blit(self.spritesheet.img_at(*self.director.worldmap[block_spot]), self.map_rect(i, j))
                if block_spot in all_players.keys():
                    if all_players[block_spot].hp > 0:
                        screen.blit(self.spritesheet.img_at(*all_players[block_spot].sprite_pos), self.map_rect(i, j))

    def on_event(self, event):
        if event.type == KEYDOWN:
            new_pos = (self.director.player.pos[0] + (-1 if event.key == K_LEFT else 0) + (1 if event.key == K_RIGHT else 0),
                       self.director.player.pos[1] + (-1 if event.key == K_UP else 0) + (1 if event.key == K_DOWN else 0))
            if new_pos not in self.director.worldmap.map_dict:
                self.director.player.pos = new_pos

    def on_update(self):
        for pos, m in self.director.monsters.items():
            if self.director.player.pos == pos and m.hp > 0:
                fight = scene_fight.SceneFight(self.director, m)
                fight.next = self
                self.director.set_scene(fight)

    def map_rect (self, i, j):
        return pygame.Rect(i*self.block, j*self.block, self.block, self.block)
