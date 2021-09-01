class Item (object):
    def __init__(self, type, name, stat):
        self.name = name
        self.type = type
        self.stat = stat

    def __repr__(self):
        return "{} {}: {} {}".format(self.type, self.name, self.stat)

def load_items():
    items = [Item("W", "fist", 0),
             Item("W", "knife", 2),
             Item("W", "sword", 5),
             Item("W", "broadsword", 7),
             Item("W", "pistol", 9),
             Item("W", "shotgun", 12),
             Item("A", "clothes", 0),
             Item("A", "bronze", 3),
             Item("A", "silver", 5),
             Item("A", "golden", 7) ]
    return { i.name: i for i in items }

