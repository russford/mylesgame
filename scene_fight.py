import pygame
import pygame.gfxdraw
import scene
import random

from pygame.locals import (
    K_BACKSPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
)

class ActionIcon (pygame.sprite.Sprite):
    def __init__(self, filename, size, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale (self.image, (size,size))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)



class SceneFight (scene.Scene):
    def __init__(self, director, enemy):
        scene.Scene.__init__(self, director)
        self.strings = []
        self.active_text = ""
        self.enemy = enemy
        self.getting_input = False
        self.frame_rects = None
        self.sprites = pygame.sprite.Group()

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.strings.append (self.active_text)
                self.getting_input = False
            elif event.key == K_ESCAPE:
                self.active_text = ""
            elif event.key == K_BACKSPACE:
                self.active_text = self.active_text[:-1]
            else:
                self.active_text += event.unicode

    def on_display(self, screen):
        screen.fill((0,0,0))
        if not self.frame_rects: self.build_frame_rects(screen)
        for r in self.frame_rects:
            pygame.draw.rect(screen, (255, 255, 255), r)
        self.sprites.draw(screen)

        font = pygame.font.SysFont ("Arial", 16)
        renders = [font.render(s, True, (200,200,200)) for s in self.strings[-10:] + [self.active_text]]
        for i, r in enumerate(renders):
            screen.blit(r, (20, i*20))

    def on_update(self):
        if self.getting_input:
            return
        if self.active_text == "":
            self.strings.append ("what would you like to do?")
            self.getting_input = True
        else:
            if self.active_text == "attack":
                self.print (self.director.player.attack(self.enemy))
            elif self.active_text == "heal":
                player.hp = self.director.player.max_hp
                self.print("your hp is now {}".format(self.director.player.hp))
            elif self.active_text == "special":
                self.print(self.director.player.special_attack(self.enemy))
            elif self.active_text == "run":
                if random.random() < 0.70:
                    self.print("you got away!")
                    self.finish()
                else:
                    self.print("you couldn't flee!")
            else:
                print("you do nothing!")
            if self.enemy.hp > 0:
                self.print(self.enemy.attack(self.director.player))
            self.active_text = ""




    def display (self, surface):
        font = pygame.freetype.Font(None, 20)
        y = 0
        for string in self.strings + [self.active_text]:
            img = font.render_to(surface, (0, y), string, (255, 255, 255))
            y += img.h + 5

    def finish (self):
        if self.director.player.hp > 0:
            self.print("you killed {} and got {} XP!".format(self.enemy.name, self.enemy.xp))
            self.director.player.xp += self.enemy.xp
        else:
            self.print("you were slain by {}".format(self.enemy.name))
        return self.director.player.hp > 0

    def print (self, string):
        self.strings += string.split('\n')

    def build_frame_rects(self, screen):
        w = screen.get_rect().w
        h = screen.get_rect().h
        b = 5
        frames = [(0,0,b,h),
                  (0,0,w,b),
                  (w-b,0,b,h),
                  (0,h-b,w,b),
                  (0,3*h//4,w,b),
                  (w//4,3*h//4,b,h//4),
                  (w//2,3*h//4,b,h//4),
                  (3*w//4,3*h//4,b,h//4),
                  ]
        self.frame_rects = [pygame.rect.Rect(*r) for r in frames]

        sprites = [("sword.png", 2*w//16, 7*h//8),
                   ("shield.png", 6*w//16, 7*h//8),
                   ("bag.png", 10*w//16, 7*h//8),
                   ("run.png", 14*w//16, 7*h//8)
                   ]

        size = min (w//8 - 4*b, h//4 - 4*b)

        for filename, cx, cy in sprites:
            self.sprites.add (ActionIcon ("images/"+filename, size, cx, cy))

