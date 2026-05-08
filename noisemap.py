import numpy as np
from noise import pnoise2
import matplotlib.pyplot as plt

width = 200
height = 200
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

terrain = np.zeros((height, width))

for i in range(height):
    for j in range(width):
        terrain[i][j] = pnoise2(i / scale,
                                j / scale,
                                octaves=octaves,
                                persistence=persistence,
                                lacunarity=lacunarity,
                                repeatx=width,
                                repeaty=height,
                                base=42)
        
normalized_terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())

print(normalized_terrain)

# Grayscale heightmap
plt.imshow(normalized_terrain, cmap='gray')
plt.title("Grayscale Heightmap")
plt.colorbar()
# plt.show()

# Colored elevation map
plt.imshow(normalized_terrain, cmap='terrain')
plt.title("Colored Terrain Elevation")
plt.colorbar()

plt.imsave("generated_terrain.png", normalized_terrain, cmap='terrain')