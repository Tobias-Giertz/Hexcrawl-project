def get_axial(col:int, row:int):
    q = col - (row // 2)
    r = row
    return q, r

def get_cube(col:int, row:int):
    q, r = get_axial(col, row)
    x, z = q, r
    y = -x - z
    return x, y, z

def coord_to_cell(col1, row1, col2=None, row2=None):
    # Convert zero-based (col,row) → 'A1' or range 'A1:B2'
    def to_letters(c):
        letters = ''
        while c >= 0:
            letters = chr(c % 26 + ord('A')) + letters
            c = c // 26 - 1
        return letters
    a1 = f"{to_letters(col1)}{row1 + 1}"
    if col2 is not None and row2 is not None:
        b1 = f"{to_letters(col2)}{row2 + 1}"
        return f"{a1}:{b1}"
    return a1

if __name__ == "__main__":
    x = 1
    y = 1

    axial = get_axial(x, y)
    cube = get_cube(x,y)
    cell = coord_to_cell(x, y)

    print(axial, cube, cell)