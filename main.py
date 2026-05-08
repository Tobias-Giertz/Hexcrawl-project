from world import World
from actor import Actor
from roads import *
from terrain import Terrain
from coordinates import axial_to_pixel



world = World.load("savegame.json")

# world.map.print_map()

# goblin_hex = world.map.get_hex(2, 3)
# actor = Actor("Goblins", goblin_hex)
# world.add_actor(actor)

world.draw_map("world.png")

# tile_a = world.map.get_hex(2, 3)
# tile_b = world.map.get_hex(3, 3)
# tile_c = world.map.get_hex(4, 4)
# tile_d = world.map.get_hex(4, 5)

# world.map.road_network.add_road(tile_a, tile_b)
# world.map.road_network.add_road(tile_b, tile_c)
# world.map.road_network.add_road(tile_c, tile_d)

# world.save("savegame.json")
