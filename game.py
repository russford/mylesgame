import pygame

import director
import scene_map

pygame.init()

game = director.Director()
game.load_file("assets/map.txt")

# map_scene = scene_editor.SceneEditor(game)
map_scene = scene_map.SceneMap(game)
game.set_scene(map_scene)

game.loop()
