import re
import numpy as np

with open(r'./input.txt') as f:
    data = f.read()

# remove all non numeric characters
data = re.findall(r'\d+', data)
# convert to (n x 4) array with columns: x1, y1, x2, y2
data = np.array(data).astype(int).reshape((-1, 4))

max_val = data.max() + 1
# create square grid
grid = np.zeros((max_val, max_val))


# part 1

# keep only horizontal or vertical lines
# (where x1 = x2 or y1 = y2)
hv_data = data[(data[:, 0] == data[:, 2]) | (data[:, 1] == data[:, 3])]
for x1, y1, x2, y2 in hv_data:
    # swap coordinates to ensure slicing from low to high
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    grid[x1:x2 + 1, y1:y2 + 1] += 1

answer = np.sum(grid >= 2)
print(answer)


# part 2
diag_data = data[(data[:, 0] != data[:, 2]) & (data[:, 1] != data[:, 3])]
for x1, y1, x2, y2 in diag_data:
    xstep = -1 if x2 < x1 else 1
    ystep = -1 if y2 < y1 else 1
    grid[
        np.arange(x1, x2 + xstep, xstep),
        np.arange(y1, y2 + ystep, ystep)
    ] += 1

answer2 = np.sum(grid >= 2)
print(answer2)
