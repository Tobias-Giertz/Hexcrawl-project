import json
import matplotlib.pyplot as plt

from map import Map
from actor import Actor
from coordinates import axial_to_pixel
from terrain import Terrain

class World:
    def __init__(self):
        self.map = Map()
        self.actors = []
        # self.clock = None

    def to_dict(self):
        return {
            "save_version": 1,
            "map": self.map.to_dict(),
            "actors": [actor.to_dict() for actor in self.actors],
            # "clock": self.clock.to_dict() if self.clock else None,
        }

    @classmethod
    def from_dict(cls, data):
        world = cls()

        world.map = Map.from_dict(data["map"])

        world.actors = [
            Actor.from_dict(actor_data, world.map)
            for actor_data in data["actors"]
        ]

        # world.clock = ...

        return world
    
    def save(self, filepath):
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        return cls.from_dict(data)
    
    def add_actor(self, actor):
        self.actors.append(actor)

####==============================####

    def list_world_objects(self):
        if not self.map.hexes:
            print("(empty map)")
            return

        for hex in self.map.hexes:
            q, r = hex
            data = self.map.get_hex(q, r)
            print(f'Hex at: {data.q}, {data.r} - {data.terrain}')

        if not self.actors:
            print("(no actors)")
            return

        for actor in self.actors:
            name = actor.name
            q, r = actor.current_hex.q, actor.current_hex.r
            print(f'Actor: {name}, at ({q}, {r})')
        return
        
    def draw_map(self, filename="plot.png"):
        terrain_colors = {
            Terrain.PLAINS: "yellow",
            Terrain.FOREST: "green",
            Terrain.MOUNTAIN: "gray",
            Terrain.SEA: "blue",
        }

        xs = []
        ys = []
        colors = []

        plt.figure(figsize=(8, 8))

        for q, r in self.map.hexes:
            tile = self.map.get_hex(q, r)
            x, y = axial_to_pixel(q, r)

            xs.append(x)
            ys.append(y)
            colors.append(terrain_colors.get(tile.terrain, "black"))

        plt.scatter(
            xs,
            ys,
            s=1000,
            c=colors,
            marker="h"
        )

        for q, r in self.map.hexes:
            x, y = axial_to_pixel(q, r)

            plt.text(
                x,
                y,
                f"{q},{r}",
                ha="center",
                va="center",
                fontsize=7,
                color="black"
            )

        for road in self.map.road_network.roads:
            a, b = tuple(road)

            a_x, a_y = axial_to_pixel(a.q, a.r)
            b_x, b_y = axial_to_pixel(b.q, b.r)

            plt.plot([a_x, b_x], [a_y, b_y], color="black")

        actor_xs = []
        actor_ys = []

        for actor in self.actors:
            if actor.current_hex is None:
                continue

            x, y = axial_to_pixel(actor.current_hex.q, actor.current_hex.r)
            actor_xs.append(x)
            actor_ys.append(y)

        plt.scatter(
            actor_xs,
            actor_ys,
            s=50,
            c="red",
            marker="o"
        )

        plt.axis("equal")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()