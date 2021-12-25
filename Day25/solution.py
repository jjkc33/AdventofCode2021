

def print_grid(east, south):
    """Helper function to visualize sea cucumber map"""
    for j in range(max_south):
        s = []
        for k in range(max_east):
            if (j, k) in east:
                s.append('>')
            elif (j, k) in south:
                s.append('v')
            else:
                s.append('.')
        print(''.join(s))


grid = []
with open(r'./input.txt') as f:
    for line in f:
        grid.append(list(line.strip()))


# 137 x 139 grid (rows = N/S, columns = E/W)
max_east = len(grid[0])
max_south = len(grid)

east, south = [], []
for i in range(max_south):
    for j in range(max_east):
        if grid[i][j] == '>':
            east.append((i, j))
        elif grid[i][j] == 'v':
            south.append((i, j))

east = set(east)
south = set(south)

print_grid(east, south)

current_spaces = east | south
occupied = set()
i = 0
while current_spaces != occupied:
    current_spaces = east | south

    east_moves = []
    for x, y in east:
        y2 = y + 1 if y + 1 < max_east else 0
        if (x, y2) in current_spaces:
            east_moves.append((x, y))
        else:
            east_moves.append((x, y2))

    east = set(east_moves)

    occupied = east | south
    south_moves = []
    for x, y in south:
        x2 = x + 1 if x + 1 < max_south else 0
        if (x2, y) in occupied:
            south_moves.append((x, y))
        else:
            south_moves.append((x2, y))

    south = set(south_moves)
    occupied = east | south
    i += 1


# part 1
print(f'{i} steps.')
print_grid(east, south)
