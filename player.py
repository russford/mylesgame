import random

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

    def attack (self, target):
        damage = random.randint (0, self.strength)
        if self.weapon: damage += random.randint (0, self.weapon.stat)
        if target.armor: damage -= random.randint(0, target.armor.stat)
        if damage < 0: damage = 0
        if damage == 0:
            print ("{} missed!".format(self.name))
        else:
            print ("{} did {} damage to {}!".format(self.name, damage, target.name))
            target.hp -= damage

    def special_attack (self, target):
        if random.randint(0,1):
            print ("special attack succeeded! {} dies immediately!".format(target.name))
            target.hp = 0
        else:
            print ("special attack failed!")

    def equip (self, item):
        if item.type == "A":
            self.armor = item
        elif item.type == "W":
            self.weapon = item
        print ("you equipped {}!".format(item.name))

    def mirror (self):
        print ("Name: {}".format(self.name))
        print ("HP: {}/{}".format(self.hp, self.max_hp))
        print ("EXP: {}".format(self.xp))
        print ("STR: {} AGL: {}".format(self.strength, self.agility))
        print ("Weapon: {} {}".format(self.weapon.name, self.weapon.stat))
        print ("Armor: {} {}".format(self.armor.name, self.armor.stat))

