import numpy as np
import pandas as pd

from config import get_section
from hex_geometry import *
from perlin_field import build_noise_mesh, render_height_3d

def get_index(df, val_col, val_row):
    mask_col = df['col'] == val_col
    mask_row = df['row'] == val_row
    matching_indices = df.index[mask_col & mask_row]
    if len(matching_indices) == 0:
        return None
    return int(matching_indices[0])



def get_neighbor_index(df, val_col, val_row):
    neighbors = get_neighbors(val_col, val_row)
    indexes = []
    for n in neighbors:
        idx = get_index(df, n[0], n[1])
        if idx is not None:
            indexes.append(idx)
    return indexes



def get_neighbor_values(df, val_col, val_row, value_col='topography', filter=None):
    neighbors_idx = get_neighbor_index(df, val_col, val_row)
    values = []
    for i in neighbors_idx:
        neighbor_val = df.iloc[i][value_col]
        if filter is not None and neighbor_val == filter:
            continue 
        values.append(neighbor_val)
    return values



def build_coordinates(cols: int, rows: int, map_id: str = "map001"):
    data = []
    index = 0
    for r in range(rows):
        for c in range(cols):
            x, y = get_cartesian(c, r)
            data.append({
                "ID": f"{map_id}-{index}-{c}-{r}",
                "col": c,
                "row": r,
                "x": x,
                "y": y
            })
            index += 1
    df = pd.DataFrame(data, columns=["ID", "col", "row", "x", "y"])
    return df



def assign_topography(df, t_mountain, t_hill, t_plains, label = "topography"):
    z = pd.to_numeric(df["noise"], errors="coerce").fillna(0.0)

    out = np.full(len(z), "water", dtype=object)

    out[z >= t_plains] = "plains"
    out[z >= t_hill] = "hill"
    out[z >= t_mountain] = "mountain"
    df[label] = out
    return df



def assign_forests(df, seed, octaves, scale, persistence, lacunarity, freq, amp, max_amp, density, bog_neighbors, label = "forest"):
    df = build_noise_mesh(df, seed + 137, octaves, scale + 6, persistence, lacunarity, freq, amp, max_amp, label = "forest_noise")
    potentials = df.index[df['topography'].isin(['plains', 'hill'])].to_numpy()
    water_idx = df.index[df['topography'].isin(['water'])].to_numpy()

    for n in water_idx:
        col, row = df.iloc[n]['col'], df.iloc[n]['row']
        n_val = get_neighbor_values(df, col, row, 'topography', 'water')
        if len(n_val) >= bog_neighbors:
            potentials = np.append(potentials, n)

    z = pd.to_numeric(df["forest_noise"], errors="coerce").fillna(0.0)

    noise_mask = z < density

    potential_mask = np.zeros(len(df), dtype=bool)
    potential_mask[potentials] = True

    forest_mask = noise_mask & potential_mask

    df[label] = forest_mask
    df = df.drop(columns=["forest_noise"])
    return df



def assign_biomes(df, config, label = "biome"):
    return df



def assign_height(df, label = "label"):
    return df



def generate_hex_map(col, row):
    config = get_section("map_settings")
    seed = config.get("seed")
    octaves = config.get("octaves")
    scale = config.get("scale")
    persistence = config.get("persistence")
    lacunarity = config.get("lacunarity")
    freq = config.get("freq")
    amp = config.get("amp")
    max_amp = config.get("max_amp")
    t_mountain = config.get("t_mountain"),
    t_hill = config.get("t_hill"),
    t_plains = config.get("t_plains")
    density = config.get("forest_density")
    bog_neighbors = config.get("bog_neighbors")

    # koordinater
    df = build_coordinates(col, row)

    # noise
    df = build_noise_mesh(df, seed, octaves, scale, persistence, lacunarity, freq, amp, max_amp)

    # topografi
    df = assign_topography(df, t_mountain, t_hill, t_plains)

    # skog
    df = assign_forests(df, seed, octaves, scale, persistence, lacunarity, freq, amp, max_amp, density, bog_neighbors)

    # biom
    df = assign_biomes(df, config)

    # höjd
    # assign_height

    # resnsa worksheet

    # exportera till worksheet

    return df
# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    """
    Debug section
    """
    def test_settings():
        cfg = get_section("hex_mapgeneration")
        print("perlin_field settings:", cfg)
        return

    # test_settings()

    cols = 24
    rows = 18

    col = 2
    row = 2

    # col_row_rairs = list(zip(map_df['col'], map_df['row']))

    map_df = generate_hex_map(cols, rows)
    # render_height_3d(map_df)
    print(map_df)
    # print("Antal celler: ", col * row)

    # print(get_index(map_df,col,row))
    # print('Neighboring indexes of ', col,',', row, ': ', get_neighbor_index(map_df, col, row))