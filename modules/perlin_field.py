import numpy as np
import pandas as pd

from config import get_section
from hex_geometry import get_cartesian

# ------------ Functions ------------

def _perlin2d(x, y, p):
    xi = np.floor(x).astype(int) & 255
    yi = np.floor(y).astype(int) & 255
    xf = x - np.floor(x)
    yf = y - np.floor(y)

    u = xf * xf * xf * (xf * (xf * 6 - 15) + 10)
    v = yf * yf * yf * (yf * (yf * 6 - 15) + 10)

    aa = p[p[xi] + yi]
    ab = p[p[xi] + yi + 1]
    ba = p[p[xi + 1] + yi]
    bb = p[p[xi + 1] + yi + 1]

    def gradient(hash, xg, yg):
        h = hash & 7
        u = np.where(h < 4, xg, yg)
        v = np.where((h == 12) | (h == 14), xg,
            np.where(h < 4, yg, xg))
        s1 = np.where((h & 1) == 0, u, -u)
        s2 = np.where((h & 2) == 0, v, -v)
        return s1 + s2
    
    x1 = gradient(aa, xf,     yf)
    x2 = gradient(ba, xf-1.0, yf)
    y1 = x1 + (x2 - x1) * u

    x1 = gradient(ab, xf,     yf-1.0)
    x2 = gradient(bb, xf-1.0, yf-1.0)
    y2 = x1 + (x2 - x1) * u

    return y1 + (y2 - y1) * v



def _permutation_table(seed: int):
    rng = np.random.RandomState(seed)
    p = np.arange(256, dtype=int)
    rng.shuffle(p)
    p = np.concatenate([p, p])  # length 512
    return p 



def build_noise_mesh(df, config, offset = 0, label = "noise"):
    seed = config.get("seed") + offset
    octaves = config.get("octaves")
    scale = config.get("scale")
    persistence = config.get("persistence")
    lacunarity = config.get("lacunarity")
    freq = config.get("freq")
    amp = config.get("amp")
    max_amp = config.get("max_amp")

    if ('x' not in df.columns) or ('y' not in df.columns):
        if ('col' not in df.columns) or ('row' not in df.columns):
            raise KeyError("Dataframe missing x, y, col or row.")
        x, y = get_cartesian(df['col'], df['row'])
    else:
        x, y = df['x'].to_numpy(), df['y'].to_numpy()

    p = _permutation_table(seed)
    total = np.zeros_like(x, dtype=float)
    for _ in range(octaves):
        nx = (x * freq) / max(1e-9, scale)
        ny = (y * freq) / max(1e-9, scale)
        total += amp * _perlin2d(nx, ny, p)
        max_amp += amp
        amp *= persistence
        freq *= lacunarity

    noise = (total / max_amp) * 0.5 + 0.5
    df[label] = noise.astype("float32")
    return df



import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
def render_height_3d(df, *, z_col="noise", title="Height 3D"):
    if z_col not in df.columns:
        raise KeyError(f"'{z_col}' column not found in DataFrame.")

    if ('x' not in df.columns) or ('y' not in df.columns):
        if ('col' not in df.columns) or ('row' not in df.columns):
            raise KeyError("Dataframe missing x, y, col or row.")
        x, y = get_cartesian(df['col'], df['row'])
    else:
        x, y = df['x'].to_numpy(), df['y'].to_numpy()

    z = pd.to_numeric(df[z_col], errors="coerce").to_numpy()

    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[m], y[m], z[m] # type: ignore
    if len(x) < 3:
        raise ValueError("Not enough valid points.")

    tri = Triangulation(x, y)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection="3d")
    ax.plot_trisurf(tri, z, linewidth=0.2, antialiased=True)

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel(z_col)
    plt.show()



# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    def test_settings():
        cfg = get_section("map_settings")
        frequency = cfg.get("frequency")
        octaves = cfg.get("octaves")
        seed = cfg.get("seed")
        print("perlin_field settings:", cfg)
        return frequency, octaves, seed

    x = 24
    y = 18
    
    data = []
    for i in range(x):
        for j in range(y):
            data.append({
                "col": i,
                "row": j
            })
    df = pd.DataFrame(data, columns=["col", "row"])

    config = get_section("map_settings")
    # seed = config.get("seed")
    # octaves = config.get("octaves")
    # scale = config.get("scale")
    # persistence = config.get("persistence")
    # lacunarity = config.get("lacunarity")
    # freq = config.get("freq")
    # amp = config.get("amp")
    # max_amp = config.get("max_amp")

    df = build_noise_mesh(df, config)
    
    render_height_3d(df)