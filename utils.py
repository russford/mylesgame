import pygame


class TextBlit (object):
    def __init__(self, fontname="Arial", fontsize="12", color=(255, 255, 255), spacing=4):
        self.change_font(fontname, fontsize)
        self.color = color
        self.spacing = spacing

    def change_font(self, fontname, fontsize):
        self.font = pygame.font.SysFont(fontname, fontsize)

    def surface(self, strings):
        renders = [self.font.render(s, True, self.color) for s in strings]
        w = max(r.get_rect().w for r in renders)
        h = sum(r.get_rect().h for r in renders) + self.spacing * (len(renders) - 1)
        surf = pygame.surface.Surface((w, h))
        y = 0
        for r in renders:
            surf.blit(r, (0, y))
            y += r.get_rect().h + self.spacing
        return surf

    def __call__(self, strings):
        return self.surface(strings)


class SpriteSheet (object):
    def __init__(self, filename, w, h, color_key=None):
        self.image = pygame.image.load(filename).convert()
        self.w = w
        self.h = h
        self.color_key = color_key
        self.image.set_colorkey(color_key)

    def img_at (self, x, y, size=0):
        if self.color_key is None:
            self.color_key = self.image.get_at((0,0))
        surface = pygame.surface.Surface((self.w, self.h))
        surface.blit(self.image, (0,0), pygame.rect.Rect(x*self.w, y*self.h, (x+1)*self.w, (y+1)*self.h))
        if size:
            surface = pygame.transform.scale(surface, (size, size))
        surface.set_colorkey(self.color_key)
        return surface

    def img_fra (self, fra_x, fra_y):
        at_x = (fra_x * self.image.get_rect().w) // self.w
        at_y = (fra_y * self.image.get_rect().h) // self.h
        return at_x, at_y

    def scaled_sheet (self, scale_factor):
        return pygame.transform.scale(self.image,
                                      (int(self.image.get_rect().w * scale_factor),
                                       int(self.image.get_rect().h * scale_factor)))


class Button (object):
    def __init__(self, text, fontname="Arial", fontsize=20, fontcolor=(255, 255, 255)):
        self.text = text
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.surface = None
        self.on_click = None
        self.rect = None

    def on_update(self):
        font = pygame.font.Font (self.fontname, self.fontsize)
        render = font.render(self.text, True, self.fontcolor)
        self.surface = pygame.surface.Surface((2 * render.get_rect().h, render.get_rect().w + 2 * render.get_rect().h))
        self.surface.fill ((255, 255, 255))
        self.surface.subsurface(self.surface.get_rect().inflate(-2, -2)).fill((0, 0, 0))
        self.surface.blit (render, (render.get_rect().h, render.get_rect().h // 2))
        self.rect = self.surface.get_rect()

    def get_surface (self):
        if self.surface is None:
            self.on_update()
        return self.surface




