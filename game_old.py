from player import Player
import item
import random

def build_enemies ():
    enemies = [["Goblin", 10, 5, 0, 2],
               ["Goblin Archer", 5, 10, 0, 3],
               ["Skeleton", 10, 7, 0, 5],
               ["Skeleton Archer", 10, 10, 0, 6]
    ]
    return {e[0]: Player(*e) for e in enemies}

def fight (player, enemy):
    enemy.hp = enemy.max_hp
    print ("{} appeared!".format(enemy.name))
    while player.hp > 0 and enemy.hp > 0:
        print ("{}: HP {}/{}".format(player.name, player.hp, player.max_hp))
        print ("{}: HP {}/{}".format(enemy.name, enemy.hp, enemy.max_hp))
        action = input("what do you do (attack, heal, special, run)?")
        if action == "attack":
            player.attack (enemy)
        elif action == "heal":
            player.hp = player.max_hp
            print ("your hp is now {}".format(player.hp))
        elif action == "special":
            player.special_attack (enemy)
        elif action == "run":
            if random.random() < 0.70:
                print ("you got away!")
                return 1
            else:
                print ("you couldn't flee!")
        else:
            print ("you do nothing!")
        if enemy.hp > 0:
            enemy.attack (player)

    if player.hp > 0:
        print ("you killed {}!".format(enemy.name))
        player.xp += enemy.xp
    else:
        print ("you were slain by {}".format(enemy.name))
    return player.hp > 0


if __name__ == "__main__":
    # name = input("Please enter your character's name: ")
    p = Player ("Myles", 20, 10, 10, 0)
    enemies = build_enemies()
    items = item.load_items()
    p.equip(items["fist"])
    p.equip(items["clothes"])

    while True:
        action = input ("What would you like to do? ")
        if action == "quit":
            break
        if action == "fight":
            n = random.choice(list(enemies.keys()))
            e = enemies[n]
            result = fight (p, e)
            if not result: break
        if action == "camp":
            p.hp = p.max_hp
            print ("you rested at camp and now have full hp!")
        if action == "mirror":
            print ("you look in the mirror!")
            p.mirror()
        if action == "give":
            item_name = input ("what item do you want?")
            if item_name in items:
                p.equip (items[item_name])
            else:
                print ("that item doesn't exist!")

    print ("game over!")




