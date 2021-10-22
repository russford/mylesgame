import pygame
import scene
import button
import utils

from pygame.locals import (
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    MOUSEBUTTONDOWN
)


class SceneSelectorPanel(scene.Scene):
    def __init__(self, director, spritesheet):
        scene.Scene.__init__(self, director)
        self.spritesheet = spritesheet
        self.sel = (0, 0)
        self.img_rect = None

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            fra_x = event.pos[0] / self.img_rect.w
            fra_y = event.pos[1] / self.img_rect.h
            self.sel = self.spritesheet.img_fra(fra_x, fra_y)
            self.director.set_scene(self.next)

    def on_update(self):
        pass

    def on_display(self, screen):
        screen.fill((0, 0, 0))
        scale_factor = min(screen.get_rect().w / self.spritesheet.image.get_rect().w,
                           screen.get_rect().h / self.spritesheet.image.get_rect().h)
        sheet = self.spritesheet.scaled_sheet(scale_factor)
        screen.blit(self.spritesheet.scaled_sheet(scale_factor), (0, 0))
        self.img_rect = sheet.get_rect()

    def sel_sprite(self, size=0):
        return self.spritesheet.img_at(*self.sel, size)


class SceneEditor (scene.Scene):
    def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.spritesheet = utils.SpriteSheet("assets/colored_packed.png", 16, 16)
        self.map_x, self.map_y = 0, 0
        self.map_size = 24
        self.map_rect = None
        self.selector_panel = SceneSelectorPanel (director, self.spritesheet)
        self.selector_panel.next = self
        self.build_buttons()

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.map_rect.collidepoint(event.pos):
                img_size = self.map_rect.w // self.map_size
                x = int((event.pos[0] - self.map_rect.left) // img_size) + self.map_x
                y = int((event.pos[1] - self.map_rect.top) // img_size) + self.map_y
                self.director.worldmap.map_dict[x, y] = self.selector_panel.sel
            for b in self.buttons:
                if b.rect.collidepoint(event.pos):
                    b.on_click()

    def on_display(self, screen):
        screen.fill((0, 0, 0))
        map_surf = pygame.surface.Surface ((screen.get_rect().w * 9 // 10, screen.get_rect().h))
        sel_block = self.selector_panel.sel_sprite(screen.get_rect().w // 10)
        screen.blit (sel_block, (0, 0))
        self.draw_map(map_surf)
        self.map_rect = map_surf.get_rect().move((sel_block.get_rect().w, 0))
        screen.blit(map_surf, self.map_rect)
        for b in self.buttons:
            screen.blit (b.surface, b.rect)

    def draw_map (self, surface):
        img_size = surface.get_rect().w // self.map_size
        for pos, img in self.director.worldmap.map_dict.items():
            if 0 <= pos[0]-self.map_x <= self.map_size and 0 <= pos[1]-self.map_y <= self.map_size:
                surface.blit(self.spritesheet.img_at(*img, img_size), (pos[0]*img_size, pos[1]*img_size))

    def on_save(self):
        self.director.worldmap.save("map.json")

    def on_load(self):
        self.director.worldmap.load("map.json")

    def on_tool(self):
        self.buttons[0].make_dirty()
        self.director.set_scene(self.selector_panel)

    def build_buttons(self):
        tool_button = button.ImageButton(self.selector_panel.sel_sprite, self.on_tool)
        tool_button.h = 2 * tool_button.h
        self.buttons = [tool_button,
                        button.TextButton("Save", self.on_save),
                        button.TextButton("Load", self.on_load)]

        width = max([b.w for b in self.buttons])
        for b in self.buttons:
            b.w = width

        self.buttons[0].topleft = (0,0)
        for i in range(1, len(self.buttons)):
            self.buttons[i].topleft = self.buttons[i-1].rect.bottomleft

    def on_update(self):
        pass


