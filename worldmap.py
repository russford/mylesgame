import json


class WorldMap (object):
    def __init__(self):
        self.map_dict = {}

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump([(k, v) for k, v in self.map_dict.items()], f)

    def load(self, filename):
        with open(filename, "r") as f:
            self.map_dict = {tuple(a[0]): tuple(a[1]) for a in json.load(f)}

    def __getitem__(self, item):
        return self.map_dict[item]

    def __setitem__(self, key, value):
        self.map_dict[key] = value
