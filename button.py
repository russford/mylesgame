import pygame


class Button (object):
    def __init__(self, on_click=None):
        self._surface = None
        self._rect = None
        self.on_click = on_click
        self.on_update()

    def on_update(self):
        raise NotImplementedError("Button.on_update() should not be called")

    @property
    def surface(self):
        if self._surface is None:
            self.on_update()
        return self._surface

    @property
    def rect(self):
        return self._rect

    def set_w(self, w):
        self._rect.w = w
        self.on_update()

    def set_h(self, h):
        self._rect.h = h
        self.on_update()

    def set_topleft(self, pos):
        self._rect.topleft = pos

    w = property(lambda self: self._rect.w, set_w)
    h = property(lambda self: self._rect.h, set_h)
    topleft = property(lambda self: self._rect.topleft, set_topleft)


class TextButton (Button):
    def __init__(self, text, on_click, fontname="Arial", fontsize=16, fontcolor=(255, 255, 255)):
        self.text = text
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        Button.__init__(self, on_click)

    def on_update(self):
        font = pygame.font.SysFont(self.fontname, self.fontsize)
        render = font.render(self.text, True, self.fontcolor)
        if self._rect is None:
            self._rect = pygame.rect.Rect((0, 0),
                                          (render.get_width() + 2 * render.get_height(), 2 * render.get_height()))
        self._surface = pygame.surface.Surface((self._rect.w, self._rect.h))
        pygame.draw.rect(self._surface, (255, 255, 255), (0, 0, self._rect.w, self._rect.h), 2, 10)
        self._surface.blit(render,
                           ((self._rect.w - render.get_width()) // 2,
                            (self._rect.h - render.get_height()) // 2))


class ImageButton (Button):
    def __init__(self, image_func, on_click):
        self.image_func = image_func
        self._image = None
        self.is_dirty = True
        Button.__init__(self, on_click)

    def on_update(self):
        if self._image is None:
            self._image = self.image_func()
            if self._rect is not None:
                scale_factor = min((self._rect.w - 20) / self._image.get_width(),
                                   (self._rect.h - 20) / self._image.get_height())
                self._image = pygame.transform.scale(self._image,
                                                     (int(self._image.get_width() * scale_factor),
                                                      int(self._image.get_height() * scale_factor)))
        if self._rect is None:
            self._rect = self._image.get_rect().inflate(10, 10)
        self._surface = pygame.surface.Surface((self._rect.w, self._rect.h))
        pygame.draw.rect(self._surface, (255, 255, 255), (0, 0, self._rect.w, self._rect.h), 2, 10)
        self._surface.blit(self._image,
                           ((self._rect.w - self._image.get_width()) // 2,
                            (self._rect.h - self._image.get_height()) // 2))

    def make_dirty(self):
        self._image = None
        self._surface = None
