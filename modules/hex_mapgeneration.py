import hex_datastore
import perlin_field

import pandas as pd



def build_coordinates(cols: int, rows: int):
    data = []
    for r in range(rows):
        for c in range(col):
            data.append({
                "ID": f"{c}"
                "col": c,
                "row": r
            }),
    df = pd.DataFrame(data, columns=["ID", "col", "row"])
    return df



def assign_noise():
    return



def assign_topography():
    return



def assign_forests():
    return



def assign_biomes():
    return



def assign_height():
    return



def generate_hex_map(columns, rows):

    # ladda .json

    # koordinater
    # build_coordinates

    # noise
    # assign_noise

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

    return # map
# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":

    columns = 10
    rows = 10

    generate_hex_map(columns, rows)