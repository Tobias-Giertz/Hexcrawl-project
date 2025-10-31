from hex_geometry import get_planar_coords
from perlin_field import noise_mesh

import pandas as pd

def build_coordinates(cols: int, rows: int, map_id: str = "map001"):
    data = []
    index = 0
    for r in range(rows):
        for c in range(cols):
            data.append({
                "ID": f"{map_id}-{index}-{c}-{r}",
                "col": c,
                "row": r
            })
            index += 1
    df = pd.DataFrame(data, columns=["ID", "col", "row"])
    return df



def assign_noise(df, seed, label = "noise"):
    x_y = df.apply(lambda r: get_planar_coords(r['col'], r['row']), axis=1)
    df['x'], df['y'] = zip(*x_y)

    df = noise_mesh(
        df, 
        seed = 0,
        amp = 1.0,
        freq = 1.0,
        max_amp = 0.0,
        octaves = 4,
        scale = 12,
        persistence = 0.5,
        lacunarity = 2.0,
        label = "noise"
        )

    return df



def assign_topography(df, label = "base"):
    return df



def assign_forests(df, seed, label = "foliage"):
    return df



def assign_biomes(df, label = "biome"):
    return df



def assign_height(df, label = "label"):
    return df



def generate_hex_map(col, row, seed):

    # ladda .json

    # koordinater
    df = build_coordinates(col, row, seed)

    # noise
    df = assign_noise(df, seed, label = "noise")

    # topografi
    # assign_topography

    # skog
    # assign_forests

    # biom
    # assign_biomes

    # höjd
    # assign_height

    # resnsa worksheet

    # exportera till worksheet

    return df
# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":

    col = 8
    row = 5
    seed = 1

    # generate_hex_map(columns, rows)
    # col_row_rairs = list(zip(map_df['col'], map_df['row']))

    map_df = generate_hex_map(col, row, seed)
    print(map_df)
