def get_axial(col_row:int):
    q = col_row[0] - (col_row[1] // 2)
    r = col_row[1]
    return q, r



def get_cube(col_row:int):
    x, z = get_axial(col_row)
    y = -x - z
    return x, y, z



def coord_to_cell(col_row_a, col_row_b=None):
    # Convert zero-based (col,row) → 'A1' or range 'A1:B2'
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



def get_distance(col_row_a, col_row_b):
    cell_a = get_cube(col_row_a)
    cell_b = get_cube(col_row_b)
    return int((abs(cell_a[0]-cell_b[0]) + abs(cell_a[1]-cell_b[1]) + abs(cell_a[2]-cell_b[2]))/2)



# ----------------- TEST AREA ----------------- #

if __name__ == "__main__":
    a = (1, 1)
    b = (3, 3)
    test = get_distance(a, b)
    print(test)