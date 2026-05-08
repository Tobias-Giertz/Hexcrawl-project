import random

from hex import Hex
from roads import RoadNetwork
from coordinates import DIRECTIONS
from terrain import Terrain

class Map:
    def __init__(self):
        self.hexes = {}
        self.road_network = RoadNetwork()

    def to_dict(self):
        return {
            "hexes": [h.to_dict() for h in self.hexes.values()],
            "road_network": self.road_network.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        map = cls()

        for h_data in data["hexes"]:
            hex = Hex.from_dict(h_data)
            map.hexes[(hex.q, hex.r)] = hex

        map.road_network = RoadNetwork.from_dict(data["road_network"], map)

        return map

    def add_hex(self, q, r, terrain=None):
        hex = Hex(q, r, terrain)
        self.hexes[(q, r)] = hex
        return hex

    def get_hex(self, q, r):
        return self.hexes.get((q, r))
    
    def get_neighbors(self, hex):
        q, r = hex.q, hex.r
        neighbors = []
        for direction, (dq, dr) in DIRECTIONS.items():
            nq = q + dq
            nr = r + dr
            neighbor = self.get_hex(nq, nr)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors
    
    def is_edge_hex(self, hex):
        q, r = hex.q, hex.r
        if self.get_hex(q, r) is None:
            return False  # eller raise ValueError

        return len(self.get_neighbors(q, r)) < 6


### ===================================================== ###

    def add_random_hex(self, q, r):
        seed = random.randint(1, 10)
        if seed < 2:
            terrain = Terrain.SEA
        elif seed < 5:
            terrain = Terrain.PLAINS
        elif seed < 8:
            terrain = Terrain.FOREST
        else:
            terrain = Terrain.MOUNTAIN
        self.add_hex(q, r, terrain)

    
    def print_map(self):
        if not self.hexes:
            print("(empty map)")
            return

        qs = [q for (q, r) in self.hexes]
        rs = [r for (q, r) in self.hexes]

        min_q, max_q = min(qs), max(qs)
        min_r, max_r = min(rs), max(rs)

        for r in range(min_r, max_r + 1):
            # indent varannan rad (för hex-känsla)
            indent = "  " if r % 2 else ""
            line = indent

            for q in range(min_q, max_q + 1):
                h = self.get_hex(q, r)

                if h is None:
                    line += " . "
                else:
                    line += f"{self._symbol(h)} "

            print(line)

    def _symbol(self, hex):
        if hex.terrain == Terrain.FOREST:
            return "F"
        elif hex.terrain == Terrain.PLAINS:
            return "P"
        elif hex.terrain == Terrain.MOUNTAIN:
            return "M"
        elif hex.terrain == Terrain.SEA:
            return "S"
        else:
            return "?"