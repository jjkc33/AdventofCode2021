from collections import deque

import numpy as np


with open(r'./input.txt') as f:
    data = [list(map(int, line.strip())) for line in f]

data = np.array(data, dtype=int)

# pad array with largest values before rolling
padded = np.pad(data, 1, mode='constant', constant_values=9)

# roll array in each direction to get all 4 adjacent neighbors
up = np.roll(padded, 1, axis=0)
down = np.roll(padded, -1, axis=0)
left = np.roll(padded, 1, axis=1)
right = np.roll(padded, -1, axis=1)

# find smallest neighbors (and remove border elements)
smallest_neighbor = np.minimum.reduce([up, down, left, right])[1:-1, 1:-1]

# identify valleys
valleys = data[data < smallest_neighbor]
answer = np.sum(1 + valleys)
print(answer)


def get_neighbors(graph, node):
    xmax, ymax = graph.shape
    x, y = node
    neighbors = [
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
    ]
    for x, y in neighbors:
        if x in range(xmax) and y in range(ymax):
            yield x, y


def bfs(graph, start):
    explored = set()
    frontier = deque()
    frontier.append(start)

    while len(frontier) > 0:
        node = frontier.popleft()
        for neighbor in get_neighbors(graph, node):
            if (neighbor not in explored) and graph[neighbor] != 9:
                explored.add(neighbor)
                frontier.append(neighbor)

    return len(explored)

low_points = np.argwhere(data < smallest_neighbor)
basin_sizes = np.zeros(valleys.shape[0])
for i, low_point in enumerate(low_points):
    basin_sizes[i] = bfs(data, tuple(low_point))

answer2 = np.prod(basin_sizes[np.argsort(basin_sizes)[-3:]])
print(answer2)
