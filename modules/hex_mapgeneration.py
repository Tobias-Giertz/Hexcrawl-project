import numpy as np
import pandas as pd

from config import get_section
from perlin_field import build_noise_mesh, render_height_3d

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



def assign_topography(df, t_mountain, t_hill, t_plains, label = "topography"):
    z = pd.to_numeric(df["noise"], errors="coerce").fillna(0.0)

    out = np.full(len(z), "water", dtype=object)

    out[z >= t_plains] = "plains"
    out[z >= t_hill] = "hill"
    out[z >= t_mountain] = "mountain"
    df[label] = out
    return df



def assign_forests(df, config, seed, octaves, scale, persistence, lacunarity, freq, amp, max_amp, density, bog_neighbors, label = "forest"):
    df = build_noise_mesh(df, seed + 137, octaves, 18, persistence, lacunarity, freq, amp, max_amp, label = "forest_noise")
    land_idx = df.index[df['value'].isin(['plains', 'hill'])].to_numpy()

    # neighbors = _build_neighbor_index_hex(df)
    vals = df['value'].to_numpy(dtype=object)

    shoreline = []
    for i, nbrs in enumerate(neighbors):
        if vals[i] == 'water':
            non_water = sum(vals[j] != 'water' for j in nbrs)
            if non_water >= bog_neighbors:
                shoreline.append(i)

    shoreline = np.array(shoreline, dtype=int)

    eligible_idx = np.unique(np.concatenate([land_idx, shoreline], axis=0))

    n = len(eligible_idx) // 2
    if n > 0:
        chosen = rng.choice(eligible_idx, size=n, replace=False)
        df.loc[chosen, label] = True

    return df



def assign_biomes(df, label = "biome"):
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
    # df = assign_forests(df, config, seed, octaves, scale, persistence, lacunarity, freq, amp, max_amp, density, bog_neighbors)

    # biom
    # assign_biomes

    # höjd
    # assign_height

    # resnsa worksheet

    # exportera till worksheet

    return df
# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    def test_settings():
        cfg = get_section("hex_mapgeneration")
        print("perlin_field settings:", cfg)
        return

    # test_settings()

    col = 24
    row = 18

    # col_row_rairs = list(zip(map_df['col'], map_df['row']))

    map_df = generate_hex_map(col, row)
    # render_height_3d(map_df)
    print(map_df)
