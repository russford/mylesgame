import pygame
from collections import defaultdict


class GameMap (object):
    def __init__(self, filename):
        self.map_dict = defaultdict(int)
        self.monsters = []
        with open(filename, "r") as f:
            game_map = [list(l.strip('\n')) for l in f.readlines()]
        self.map_size = (len(game_map[0]), len(game_map))
        for i in range(len(game_map)):
            for j in range(len(game_map[i])):
                if game_map[i][j] == "#":
                    self.map_dict[(j,i)] = 1
                if game_map[i][j] == "P":
                    self.p_x, self.p_y = j, i
                if game_map[i][j] == "M":
                    self.monsters.append ((i,j))
        self.block_size = 20
        self.block_count = 21

    def map_rect (self, i, j):
        return pygame.Rect(i*self.block_size, j*self.block_size, self.block_size, self.block_size)

    def render (self, surface):
        self.block_size = min(surface.get_rect().w // self.map_size[0], surface.get_rect().h // self.map_size[1])
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                if self.map_dict[(i,j)]:
                    pygame.draw.rect (surface, (128, 128, 128), self.map_rect(i, j))
        pygame.draw.rect (surface, (255,0,0), self.map_rect(self.p_x, self.p_y))
        for mx, my in self.monsters:
            pygame.draw.rect (surface, (0,255,0), self.map_rect (mx, my))


    def move (self, dir_x, dir_y):
        if (self.p_x + dir_x, self.p_y + dir_y) in self.monsters:
            pass

        if not self.map_dict[(self.p_x+dir_x, self.p_y+dir_y)]:
            self.p_x += dir_x
            self.p_y += dir_y



class Wall (pygame.sprite.Sprite):
    def __init__(self):
        super.__init__()
        self.block = pygame.Surface(20,20)
        self.block.fill((128, 128, 128))
        self.rect = self.block.get_rect()

