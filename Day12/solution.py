from collections import defaultdict, deque


edges = defaultdict(list)
nodes = set()

with open(r'./input.txt') as f:
    for line in f:
        start, end = line.strip().split('-')
        edges[start].append(end)
        edges[end].append(start)
        nodes.add(start)
        nodes.add(end)


def bfs_part1(graph, start, goal):
    valid_paths = []
    path = [start]
    frontier = deque()
    frontier.append((start, path))

    while len(frontier) > 0:
        cur_node, cur_path = frontier.pop()
        for neighbor in sorted(graph[cur_node]):
            if neighbor.islower() and neighbor in cur_path:
                continue

            new_path = list(cur_path)
            new_path.append(neighbor)
            if neighbor == goal:
                valid_paths.append(new_path)
            else:
                frontier.append((neighbor, new_path))

    return valid_paths


# part 1
paths = bfs_part1(edges, 'start', 'end')
print(len(paths))


def bfs_part2(graph, start, goal, small_caves):
    valid_paths = []
    path = [start]
    frontier = deque()
    frontier.append((start, path))

    while len(frontier) > 0:
        cur_node, cur_path = frontier.pop()
        for neighbor in sorted(graph[cur_node]):
            if neighbor == start:
                continue

            if neighbor.islower() and neighbor in small_caves:
                # invalid path if already visited a small cave twice and about to revisit a cave
                if (cur_path.count(neighbor) >= 1) and (any(cur_path.count(cave) == 2 for cave in small_caves)):
                    continue

            new_path = list(cur_path)
            new_path.append(neighbor)
            if neighbor == goal:
                valid_paths.append(new_path)
            else:
                frontier.append((neighbor, new_path))

    return valid_paths


# part 2
small_caves = {cave for cave in nodes if cave.islower() and cave not in ('start', 'end')}
paths = bfs_part2(edges, 'start', 'end', small_caves)
print(len(paths))
