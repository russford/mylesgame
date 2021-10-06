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


