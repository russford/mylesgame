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

    def img_at (self, x, y, scale=1):
        if self.color_key is None:
            self.color_key = self.image.get_at((0,0))
        surface = pygame.surface.Surface((self.w, self.h))
        surface.blit(self.image, (0,0), pygame.rect.Rect(x*self.w, y*self.h, (x+1)*self.w, (y+1)*self.h))
        if scale != 1.0: surface = pygame.transform.scale(surface, (self.w*scale, self.h*scale))
        surface.set_colorkey(self.color_key)
        return surface

