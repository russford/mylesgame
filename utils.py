import pygame


class TextBlit (object):
    def __init__(self, fontname="Arial", fontsize=12, color=(255, 255, 255), spacing=4):
        self.change_font(fontname, fontsize)
        self.color = color
        self.spacing = spacing

    def change_font(self, fontname, fontsize):
        self.font = pygame.font.SysFont(fontname, fontsize)

    def surface(self, strings):
        renders = [self.font.render(s, True, self.color) for s in strings]
        if not renders:
            return pygame.surface.Surface((0, 0))
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
        self.cols = self.image.get_width() // w
        self.rows = self.image.get_height() // h
        self.color_key = color_key if color_key is not None else self.image.get_at((0, 0))
        self._cache = {}
        self._scaled = (None, None)

    def img_at(self, x, y, size=0):
        key = (x, y, size)
        surface = self._cache.get(key)
        if surface is None:
            surface = pygame.surface.Surface((self.w, self.h))
            surface.blit(self.image, (0, 0), pygame.rect.Rect(x * self.w, y * self.h, self.w, self.h))
            if size:
                surface = pygame.transform.scale(surface, (size, size))
            surface.set_colorkey(self.color_key)
            self._cache[key] = surface
        return surface

    def img_fra(self, fra_x, fra_y):
        """Tile coordinates at a fractional position of the sheet, or None if outside it."""
        if not (0 <= fra_x < 1 and 0 <= fra_y < 1):
            return None
        return int(fra_x * self.cols), int(fra_y * self.rows)

    def scaled_sheet(self, scale_factor):
        if self._scaled[0] != scale_factor:
            self._scaled = (scale_factor, pygame.transform.scale(
                self.image,
                (int(self.image.get_rect().w * scale_factor),
                 int(self.image.get_rect().h * scale_factor))))
        return self._scaled[1]
