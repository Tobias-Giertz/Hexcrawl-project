import hex_geometry
import hex_datastore
import perlin_field

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
    for col, row in zip(df['col'], df['row']):
        print(col, row)

    noise = 1
    df[label] = noise
    return df



def assign_topography(df, label = "base"):
    return df



def assign_forests(df, seed, label = "foliage"):
    return df



def assign_biomes(df, label = "biome"):
    return df



def assign_height(df, label = "label"):
    return df



def generate_hex_map(columns, rows, seed):

    # ladda .json

    # koordinater
    df = build_coordinates(columns, rows, seed)

    # noise
    # df = assign_noise(df, mesh)

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

    columns = 8
    rows = 5
    seed = 1

    # generate_hex_map(columns, rows)

    map_df = generate_hex_map(columns, rows, seed)
    col_row_rairs = list(zip(map_df['col'], map_df['row']))
    print(col_row_rairs)
