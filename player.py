import random
import pygame


class Player (object):
    def __init__(self, name, hp, strength, agility, xp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.strength = strength
        self.agility = agility
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.xp = xp
        self.pos = (0, 0)
        self.sprite_pos = (0, 0)

    def attack(self, target):
        damage = random.randint (0, self.strength)
        if self.weapon:
            damage += random.randint (0, self.weapon.stat)
        if target.armor:
            damage -= random.randint(0, target.armor.stat)
        if damage < 0:
            damage = 0
        if damage == 0:
            return "{} missed!".format(self.name)
        else:
            target.hp -= damage
            if target.hp < 0:
                target.hp = 0
            return "{} did {} damage to {}!".format(self.name, damage, target.name)

    def special_attack(self, target):
        if random.randint(0,1):
            target.hp = 0
            return "special attack succeeded! {} dies immediately!".format(target.name)
        else:
            return "special attack failed!"

    def equip(self, item):
        if item.type == "A":
            self.armor = item
        elif item.type == "W":
            self.weapon = item
        print ("you equipped {}!".format(item.name))

    def mirror(self):
        str_list = ["{}".format(self.name),
                    "HP: {}/{}".format(self.hp, self.max_hp),
                    "EXP: {}".format(self.xp),
                    "STR: {} AGL: {}".format(self.strength, self.agility)]
        if self.weapon:
            str_list.append("Weapon: {} {}".format(self.weapon.name, self.weapon.stat))
        if self.armor:
            str_list.append("Armor: {} {}".format(self.armor.name, self.armor.stat))
        return str_list







