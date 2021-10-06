import pygame
import director
import player
import scene_map
import item

pygame.init()

director = director.Director()
director.load_file("assets/map.txt")

map_scene = scene_map.SceneMap(director)
director.set_scene(map_scene)

director.loop()


