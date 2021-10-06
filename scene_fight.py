import pygame
import utils
import scene
import random

from pygame.locals import (
    K_BACKSPACE,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    MOUSEBUTTONDOWN
)


class ActionIcon (pygame.sprite.Sprite):
    def __init__(self, filename, size, cx, cy, action):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (cx, cy)
        self.action = action


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
                self.strings.append(self.active_text)
                self.getting_input = False
            elif event.key == K_ESCAPE:
                self.active_text = ""
            elif event.key == K_BACKSPACE:
                self.active_text = self.active_text[:-1]
            else:
                self.active_text += event.unicode
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for icon in [s for s in self.sprites if s.rect.collidepoint(pos)]:
                self.active_text = icon.action
                self.getting_input = False

    def on_display(self, screen):
        screen.fill((0, 0, 0))
        if not self.frame_rects:
            self.build_frame_rects(screen)
        for r in self.frame_rects:
            pygame.draw.rect(screen, (255, 255, 255), r)
        self.sprites.draw(screen)

        blitter = utils.TextBlit("Arial", 20, (255, 255, 255), 3)
        screen.blit(blitter(self.strings[-10:] + [self.active_text]), (20, 20))

        player_surf = blitter(self.director.player.mirror())
        monster_surf = blitter(self.enemy.mirror())
        w = max (player_surf.get_rect().w, player_surf.get_rect().w)
        screen.blit(player_surf, (screen.get_rect().w - w - 10, 10))
        screen.blit(monster_surf, (screen.get_rect().w - w - 10, 20 + player_surf.get_rect().h))

    def on_update(self):
        if self.enemy.hp <= 0 or self.director.player.hp <= 0:
            self.finish()
        if self.getting_input:
            return
        if self.active_text == "":
            self.strings.append("what would you like to do?")
            self.getting_input = True
        else:
            if self.active_text == "attack":
                self.do_attack()
            elif self.active_text == "heal":
                self.do_heal()
            elif self.active_text == "special":
                self.do_special()
            elif self.active_text == "run":
                self.do_run()
            else:
                self.print("you do nothing!")
            if self.enemy.hp > 0:
                self.print(self.enemy.attack(self.director.player))
            self.active_text = ""

    def finish(self, ran=False):
        if not ran:
            if self.director.player.hp > 0:
                end_msg = "you killed {} and got {} XP!".format(self.enemy.name, self.enemy.xp)
                self.director.player.xp += self.enemy.xp
                finish_scene = SceneFightEnd(self.director, "victory.png", end_msg)
                finish_scene.next = self.next
            else:
                end_msg = "you were slain by {}".format(self.enemy.name)
                finish_scene = SceneFightEnd(self.director, "defeat.png", end_msg)
                finish_scene.next = None
            self.director.set_scene (finish_scene)
        self.done = True


    def do_attack(self):
        self.print(self.director.player.attack(self.enemy))

    def do_heal(self):
        self.director.player.hp = self.director.player.max_hp
        self.print("your hp is now {}".format(self.director.player.hp))

    def do_special(self):
        self.print(self.director.player.special_attack(self.enemy))

    def do_run(self):
        if random.random() < 0.70:
            self.print("you got away!")
            self.finish(ran=True)
        else:
            self.print("you couldn't flee!")

    def print(self, string):
        self.strings += string.split('\n')

    def build_frame_rects(self, screen):
        w = screen.get_rect().w
        h = screen.get_rect().h
        b = 5
        frames = [(0,      0,      b, h),
                  (0,      0,      w, b),
                  (w-b,    0,      b, h),
                  (0,      h-b,    w, b),
                  (0,      3*h//4, w, b),
                  (w//4,   3*h//4, b, h//4),
                  (w//2,   3*h//4, b, h//4),
                  (3*w//4, 3*h//4, b, h//4),
                  ]
        self.frame_rects = [pygame.rect.Rect(*r) for r in frames]

        sprites = [("sword.png",    w//8, 7*h//8, "attack"),
                   ("shield.png", 3*w//8, 7*h//8, "heal"),
                   ("bag.png",    5*w//8, 7*h//8, "special"),
                   ("run.png",    7*w//8, 7*h//8, "run")
                   ]

        size = min(w//8 - 4*b, h//4 - 4*b)

        for filename, cx, cy, action in sprites:
            self.sprites.add(ActionIcon("assets/"+filename, size, cx, cy, action))

class SceneFightEnd (scene.Scene):
    def __init__(self, director, image_name, message):
        scene.Scene.__init__(self, director)
        image = pygame.image.load("assets/"+image_name).convert()
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(message, True, (255, 255, 255))

        w = max(text.get_rect().w, image.get_rect().w) + 20
        h = text.get_rect().h * 2 + image.get_rect().h + 20

        self.surface = pygame.surface.Surface((w, h))
        self.surface.fill ((255, 255, 255))
        pygame.draw.rect(self.surface, (0, 0, 0), self.surface.get_rect().inflate(-10, -10))

        self.surface.blit(image, ((w - image.get_rect().w)//2, 10))
        self.surface.blit(text, ((w - text.get_rect().w)//2, text.get_rect().h + image.get_rect().h + 10))

    def on_event(self, event):
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            self.director.set_scene(self.next)

    def on_update(self):
        pass

    def on_display(self, screen):
        screen.blit (self.surface,
                     ((screen.get_rect().w - self.surface.get_rect().w) // 2,
                      (screen.get_rect().h - self.surface.get_rect().h) // 2))





