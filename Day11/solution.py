import numpy as np


def get_neighbors(graph, node):
    """Get local neighbors (3x3 grid) around a given node coordinates"""
    xmax, ymax = graph.shape
    x, y = node
    graph[
         max(x - 1, 0):min(x + 2, xmax),
         max(y - 1, 0):min(y + 2, ymax),
    ] += 1
    return np.argwhere(graph > 9).tolist()


with open(r'./input.txt', mode='r') as f:
    values = [list(line.strip()) for line in f]

octopi = np.array(values, dtype=int)
steps = 100

# part 1
answer = None
flashes = 0

# part 2
step = 0
all_sync = False
while not all_sync:
    octopi += 1
    flashed = set()
    flashing = np.argwhere(octopi > 9).tolist()
    while len(flashing) > 0:
        x, y = flashing.pop()
        if (x, y) not in flashed:
            flashing.extend(get_neighbors(octopi, (x, y)))
            flashed.add((x, y))

    if flashed:
        flashes += len(flashed)
        flashed = np.array(list(flashed)).T
        octopi[flashed[0], flashed[1]] = 0

        # part 2
        if flashed.shape[1] == octopi.size:
            all_sync = True

    # part 1
    if step == 100:
        answer = flashes

    step += 1


print(answer)
print(step)
