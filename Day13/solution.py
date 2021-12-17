import numpy as np

coords = []
folds = []
with open(r'./input.txt') as f:
    for line in f:
        line = line.strip()
        if line.startswith('fold'):
            line = line.replace('fold along ', '')
            folds.append(line.split('='))
        elif line:
            coords.append(line.split(','))

coords = np.array(coords, dtype=int).T
xmax, ymax = np.max(coords, axis=1) + 1

grid = np.zeros((xmax, ymax), dtype=int)
grid[coords[0], coords[1]] = 1

for i, (fold_axis, fold_idx) in enumerate(folds):
    fold_idx = int(fold_idx)
    if fold_axis == 'y':
        folded = np.flip(grid, axis=1)
        grid = (grid | folded)[:, :fold_idx]
    else:
        folded = np.flip(grid, axis=0)
        grid = (grid | folded)[:fold_idx, :]

    if i == 0:
        # part 1
        print(grid.sum())

# format capital letters
grid = grid.reshape((-1, 5, 6))
for i in range(8):
    print(f'\nLetter {i + 1}:\n', grid[i, :, :].T)
