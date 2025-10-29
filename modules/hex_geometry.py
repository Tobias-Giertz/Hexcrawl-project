import numpy as np

def get_axial(col_row:int):
    # takes (col,row) coordinates: returns axial coordinates
    q = col_row[0] - (col_row[1]) // 2
    r = col_row[1]
    return q, r



def get_cube(col_row:int):
    # takes (col,row) coordinates: returns cube coordinates
    x, z = get_axial(col_row)
    y = -x - z
    return x, y, z



def get_coords(cube_axial):
    # takes cube or axial: returns (col,row) coordinates
    if len(cube_axial) == 3:
        x, y, z = cube_axial
        col = x + ((z - (z % 2)) // 2)
        row = z
    else:
        q, r = cube_axial
        col = q + ((r - (r % 2)) // 2)
        row = r
    return col, row



def get_distance(col_row_a, col_row_b):
    # takes (col,row) coordinates of two tiles: returns distance
    cell_a = get_cube(col_row_a)
    cell_b = get_cube(col_row_b)
    return int((abs(cell_a[0]-cell_b[0]) + abs(cell_a[1]-cell_b[1]) + abs(cell_a[2]-cell_b[2]))/2)



def get_neighbors(col_row):
    # takes (col,row) coordinates: returns (col,row) of all 6 neighbors
    axial_offsets = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    q, r = get_axial(col_row)
    return [get_coords((q + dq, r + dr)) for dq, dr in axial_offsets]



def get_cell(col_row_a, col_row_b=None):
    # takes (col,row) coordinates: returns cell designation 'A1' or range 'A1:B2'
    def to_letters(c):
        letters = ''
        while c >= 0:
            letters = chr(c % 26 + ord('A')) + letters
            c = c // 26 - 1
        return letters
    cell_a = f"{to_letters(col_row_a[0])}{col_row_a[1] + 1}"
    if col_row_b is not None:
        cell_b = f"{to_letters(col_row_b[0])}{col_row_b[1] + 1}"
        return f"{cell_a}:{cell_b}"
    return cell_a



def get_planar_coords(col_row):
    q, r = get_axial(col_row)
    x = np.sqrt(3.0) * (q + 0.5 * r)
    y = 1.5 * r
    return x, y    



# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    a = (0, 0)
    b = (0, 1)
    c = (1, 0)
    d = (1, 1)

    list_a = [(0, 0, 1, 1), (0, 1, 0, 1)]

    test = get_axial(list_a)
    print(test)