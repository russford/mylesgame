import random

import pygame

import item
import worldmap
from player import Player

WALL_TILE = (1, 1)
FPS = 60


class Director (object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.scene = None
        self.quit_flag = False
        self.player = None
        self.worldmap = worldmap.WorldMap()
        self.monsters = {}
        self.items = {}
        self.map_w, self.map_h = 0, 0

    def loop(self):
        while not self.quit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                      and self.scene.esc_quits):
                    self.quit()
                else:
                    self.scene.on_event(event)
            self.scene.on_update()
            self.scene.on_display(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def quit(self):
        self.quit_flag = True

    def load_file(self, filename):
        self.player = Player("Myles", 20, 10, 10, 0)
        self.items = item.load_items()
        self.player.equip(self.items["fist"])
        self.player.equip(self.items["clothes"])

        enemy_data = self.load_enemies("assets/enemies.txt")

        has_tiles = self.worldmap.load()

        with open(filename, "r") as f:
            game_map = [list(l.rstrip('\n')) for l in f.readlines()]
        self.map_w, self.map_h = max(len(row) for row in game_map), len(game_map)
        for y, row in enumerate(game_map):
            for x, c in enumerate(row):
                if c == "#":
                    self.worldmap.walls.add((x, y))
                    if not has_tiles:
                        # no map.json yet: draw walls with a default tile
                        self.worldmap[(x, y)] = WALL_TILE
                elif c == "P":
                    self.player.pos = (x, y)
                    self.player.prev_pos = (x, y)
                elif c == "M":
                    enemy = Player(*random.choice(enemy_data))
                    enemy.pos = (x, y)
                    self.monsters[(x, y)] = enemy

    def load_enemies(self, filename):
        enemy_data = []
        with open(filename, "r") as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                data = [d.strip() for d in line.split(",")]
                enemy_data.append([data[0]] + [int(a) for a in data[1:]])
        return enemy_data

    def set_scene(self, scene):
        if scene is None:
            self.quit_flag = True
        else:
            self.scene = scene
