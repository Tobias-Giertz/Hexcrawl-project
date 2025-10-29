import numpy as np

def _perlin2d(x, y, p):
    # x, y:
    # p: deterministic seed

    # unit grid corners
    xi = np.floor(x).astype(int) & 255
    yi = np.floor(y).astype(int) & 255
    xf = x - np.floor(x)
    yf = y - np.floor(y)

    # fade
    u = xf * xf * xf * (xf * (xf * 6 - 15) + 10)
    v = yf * yf * yf * (yf * (yf * 6 - 15) + 10)

    # hashing corners
    aa = p[p[xi] + yi]
    ab = p[p[xi] + yi + 1]
    ba = p[p[xi + 1] + yi]
    bb = p[p[xi + 1] + yi + 1]

    def gradient(hash, xg, yg):
        # gradients
        h = hash & 7
        u = np.where(h < 4, xg, yg)
        v = np.where((h == 12) | (h == 14), xg,
            np.where(h < 4, yg, xg))
        # signs
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



# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    x = 1
    y = 1
    seed = 0
    print(_perlin2d(x, y, _permutation_table(seed)))