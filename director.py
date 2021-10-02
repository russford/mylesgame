import pygame
from player import Player
import random
import item


class Director (object):
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        self.scene = None
        self.quit_flag = False
        self.player = None
        self.monsters = {}
        self.items = []
        self.map_dict = {}
        self.map_w, self.map_h = (0,0)

    def loop (self):
        while not self.quit_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.quit()
                self.scene.on_event(event)
            self.scene.on_update()
            self.scene.on_display(self.screen)
            pygame.display.flip()

    def quit(self):
        self.quit_flag = True

    def load_file (self, filename):
        self.player = Player("Myles", 20, 10, 10, 0)
        self.items = item.load_items()
        self.player.equip(self.items["fist"])
        self.player.equip(self.items["clothes"])

        enemy_data = self.load_enemies ("enemies.txt")

        with open(filename, "r") as f:
            game_map = [list(l.strip('\n')) for l in f.readlines()]
        self.map_w, self.map_h = (len(game_map[0]), len(game_map))
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == "#":
                    self.map_dict[(j, i)] = 1
                if game_map[i][j] == "P":
                    self.player.pos = (j,i)
                if game_map[i][j] == "M":
                    enemy = Player(*random.choice (enemy_data))
                    enemy.pos = (j,i)
                    self.monsters[(j,i)] = enemy

    def load_enemies (self, filename):
        enemy_data = []
        with open (filename, "r") as f:
            for line in f.readlines():
                data = [d.strip() for d in line.split(",")]
                enemy_data.append([data[0]] + [int(a) for a in data[1:]])
        return enemy_data

    def set_scene (self, scene):
        self.scene = scene










