import json
import os

MAP_FILE = os.path.join("assets", "map.json")


class WorldMap (object):
    """Visual tiles (map_dict) plus a separate set of blocking squares (walls).

    Only map_dict is saved to JSON; walls come from the text map so that
    painting a floor tile in the editor never blocks movement.
    """

    def __init__(self):
        self.map_dict = {}
        self.walls = set()

    def save(self, filename=MAP_FILE):
        with open(filename, "w") as f:
            json.dump([(k, v) for k, v in self.map_dict.items()], f)

    def load(self, filename=MAP_FILE):
        """Load visual tiles. Returns False (leaving the map unchanged) if the file is missing."""
        if not os.path.exists(filename):
            return False
        with open(filename, "r") as f:
            self.map_dict = {tuple(int(c) for c in a[0]): tuple(int(c) for c in a[1])
                             for a in json.load(f)}
        return True

    def is_blocked(self, pos):
        return pos in self.walls

    def __contains__(self, item):
        return item in self.map_dict

    def __getitem__(self, item):
        return self.map_dict[item]

    def __setitem__(self, key, value):
        self.map_dict[key] = value
