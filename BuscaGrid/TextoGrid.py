
# converte texto em grid tipo string
def converterTextoGrid(texto):
    text_input = texto

    char_grid = []

    for line in text_input.split('\n'):
        char_grid.append(list(line))

    return char_grid

# converte texto em grid tipo int
def converterTextoGridInt(texto):
    grid = converterTextoGrid(texto)
    new_grid = grid

    for index_row, row in enumerate(new_grid):
        for index_col, col in enumerate(row):
            new_grid[index_row][index_col] = int(new_grid[index_row][index_col])

    return new_grid

# converte texto em grid tipo ponderado int (separado com ",")
def converterTextoGridPonderadoInt(texto):
    text_input = texto

    char_grid = []

    for line in text_input.split('\n'):
        lista_int = [int(x) for x in line.split(',')]
        char_grid.append(lista_int)

    return char_grid

# printar grid
def printGrid(grid):
    for row in grid:
        print(row)