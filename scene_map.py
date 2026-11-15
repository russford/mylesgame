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
)

move_dict = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}


class SceneMap (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.map_x, self.map_y = 0, 0
        self.tile_size = 24
        self.spritesheet = utils.SpriteSheet("assets/colored_packed.png", 16, 16)

    def update_camera(self, screen):
        """Follow the player, without scrolling past the edges of the map."""
        cols = screen.get_width() // self.tile_size
        rows = screen.get_height() // self.tile_size
        px, py = self.director.player.pos
        self.map_x = self.clamp(px - cols // 2, self.director.map_w - cols)
        self.map_y = self.clamp(py - rows // 2, self.director.map_h - rows)
        return cols, rows

    @staticmethod
    def clamp(offset, max_offset):
        # if the map fits on screen, max_offset < 0 and the map stays anchored at the top-left
        return max(0, min(offset, max_offset))

    def on_display(self, screen):
        screen.fill((0, 0, 0))
        cols, rows = self.update_camera(screen)

        all_players = self.director.monsters | {self.director.player.pos: self.director.player}
        for i in range(cols + 1):
            for j in range(rows + 1):
                block_spot = (i + self.map_x, j + self.map_y)
                if block_spot in self.director.worldmap:
                    screen.blit(self.spritesheet.img_at(*self.director.worldmap[block_spot], self.tile_size), self.map_rect(i, j))
                character = all_players.get(block_spot)
                if character is not None and character.hp > 0:
                    screen.blit(self.spritesheet.img_at(*character.sprite_pos, self.tile_size), self.map_rect(i, j))

    def on_event(self, event):
        if event.type == KEYDOWN and event.key in move_dict:
            player = self.director.player
            dx, dy = move_dict[event.key]
            new_pos = (player.pos[0] + dx, player.pos[1] + dy)
            if not self.director.worldmap.is_blocked(new_pos):
                player.prev_pos = player.pos
                player.pos = new_pos

    def on_update(self):
        m = self.director.monsters.get(self.director.player.pos)
        if m is not None and m.hp > 0:
            fight = scene_fight.SceneFight(self.director, m)
            fight.next = self
            self.director.set_scene(fight)

    def map_rect(self, i, j):
        return pygame.Rect(i * self.tile_size, j * self.tile_size, self.tile_size, self.tile_size)
