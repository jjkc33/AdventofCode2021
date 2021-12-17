from queue import PriorityQueue


def get_neighbors(node: tuple, mode: int = 2):
    dim = 500 if mode == 2 else 100
    x, y = node
    neighbors = [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
    ]
    for n in neighbors:
        # ensure node lies within graph
        if n[0] in range(dim) and n[1] in range(dim):
            yield n


def get_node_cost(graph: dict, node: tuple):
    """ determine cost of a given node """
    x, y = node
    xtile, xpos = divmod(x, 100)
    ytile, ypos = divmod(y, 100)
    cost = graph[(xpos, ypos)]
    cost += xtile + ytile
    if cost > 9:
        cost -= 9
    return cost


def best_first_search(graph, start, goal, mode=2):
    """ Best first search of given graph from start to goal nodes """
    path = [start]
    cost = 0

    reached = {start: cost}
    frontier = PriorityQueue()
    frontier.put((cost, path))

    while not frontier.empty():
        cost, path = frontier.get()
        if path[-1] == goal:
            break

        for neighbor in get_neighbors(path[-1], mode=mode):
            new_cost = cost + get_node_cost(graph, neighbor)
            if (neighbor not in reached) or (new_cost < reached.get(neighbor, 0)):
                new_path = path + [neighbor]
                frontier.put((new_cost, new_path))
                reached[neighbor] = new_cost

    return reached[goal]


grid = {}
with open(r'./input.txt') as f:
    for i, line in enumerate(f):
        for j, num in enumerate(line.strip()):
            grid[(i, j)] = int(num)

# part 1
answer = best_first_search(grid, (0, 0), (99, 99), mode=1)
print(answer)

# part 2
answer2 = best_first_search(grid, (0, 0), (499, 499), mode=2)
print(answer2)
