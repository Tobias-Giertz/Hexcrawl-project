import json
from modules import *

with open("settings.json", "r") as f:
    settings = json.load(f)

print(settings)

# variable = perlin_field.function(settings["perlin_field"])