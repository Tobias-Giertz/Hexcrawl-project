import numpy as np

def get_axial(col:int, row:int):
    # takes (col,row) coordinates: returns axial coordinates
    q = col - ((row - (row % 2)) // 2)
    r = row
    return q, r



def get_cube(col:int, row:int):
    # takes (col,row) coordinates: returns cube coordinates
    x, z = get_axial(col, row)
    y = -x - z
    return x, y, z



def get_coords(a:int, b:int, c:int=None): # type: ignore
    # takes cube or axial: returns (col,row) coordinates
    if c is not None:
        col = a + ((c - (c % 2)) // 2)
        row = c
    else:
        col = a + ((b - (b % 2)) // 2)
        row = b
    return col, row



def get_distance(col_a:int, row_a:int, col_b:int, row_b:int):
    # takes (col,row) coordinates of two tiles: returns distance
    a_x, a_y, a_z = get_cube(col_a, row_a)
    b_x, b_y, b_z = get_cube(col_b, row_b)
    return int((abs(a_x-b_x) + abs(a_y-b_y) + abs(a_z-b_z))/2)



def get_neighbors(col:int, row:int):
    # takes (col,row) coordinates: returns (col,row) of all 6 neighbors
    axial_offsets = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    q, r = get_axial(col, row)
    return [get_coords(q + dq, r + dr) for dq, dr in axial_offsets]



def get_cell(col_a:int, row_a:int, col_b:int=None, row_b:int=None): # type: ignore
    # takes (col,row) coordinates: returns cell designation 'A1' or range 'A1:B2'
    def to_letters(c):
        letters = ''
        while c >= 0:
            letters = chr(c % 26 + ord('A')) + letters
            c = c // 26 - 1
        return letters
    cell_a = f"{to_letters(col_a)}{row_a + 1}"
    if col_b and row_b is not None:
        cell_b = f"{to_letters(col_b)}{row_b + 1}"
        return f"{cell_a}:{cell_b}"
    return cell_a



def get_cartesian(col:int, row:int):
    # transforms (col, row) to planar points
    q, r = get_axial(col, row)
    x = np.sqrt(3.0) * (q + 0.5 * r) / 1.5
    y = 1.5 * r / 1.5
    return x, y    



def get_colrow_from_cartesian(px:float, py:float):
    # transforms cartesian coordinates to (col, row)
    row = int(round(py))
    col = int(round(px * (1.5/np.sqrt(3)) - 0.5*(row % 2)))
    return col, row



# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    a = 1
    b = 1
    c = 2
    d = 2

    list_a = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4)]
    list_b = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]

    axial = get_axial(a, b)
    print('Axial:', axial)

    cube = get_cube(a, b)
    print('Cube:', cube)

    from_axial = get_coords(axial[0], axial[1])
    print('From Axial:', from_axial)

    from_cube = get_coords(cube[0], cube[1], cube[2])
    print('From Cube:', from_cube)

    distance = get_distance(a, b, c, d)
    print('Distance:', distance)

    neighbors = get_neighbors(a, b)
    print('Neighbors:', neighbors)

    cells = get_cell(a, b, c, d)
    print('Cells:', cells)

    x, y = get_cartesian(a, b)
    print('Planar:', x, y)

    colrow = get_colrow_from_cartesian(x, y)
    print('From planar:', colrow)

    coordinates = []
    for coord in list_a:
        x, y = get_cartesian(coord[0],coord[1])
        coordinates.append(get_colrow_from_cartesian(x, y))
    print(coordinates)
