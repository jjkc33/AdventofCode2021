import re
from collections import Counter


def find_intersection(c1, c2):
    """Determine intersection of two cubes, c1 and c2"""
    c3 = []
    for i in range(0, len(c1), 2):
        min_pos = max(c1[i], c2[i])
        max_pos = min(c1[i + 1], c2[i + 1])

        if min_pos > max_pos:  # no intersection found
            return None

        c3.extend([min_pos, max_pos])

    return tuple(c3)


def volume(cube):
    """Calculate volume of a given cube"""
    v = 1
    for i in range(0, len(cube), 2):
        v *= cube[i + 1] - cube[i] + 1
    return v


def find_lit_cubes(states, coords, part1=False):
    cubes = Counter()
    for s, c in zip(states, coords):
        if part1 and any(abs(i) > 50 for i in c):
            continue

        overlaps = Counter()
        for cube, count in cubes.items():
            intersect = find_intersection(cube, c)
            if intersect:  # avoid double counting intersecting cubes
                overlaps[intersect] -= count

        cubes[c] += s
        cubes.update(overlaps)

    return cubes


states, coords = [], []
with open(r'./input.txt') as f:
    for line in f:
        state, nums = line.split()
        nums = re.findall('-?\d+', nums)
        states.append(int(state == 'on'))
        coords.append(tuple(int(n) for n in nums))


# part 1
part1cubes = find_lit_cubes(states, coords, part1=True)
part1lit = sum(v * volume(c) for c, v in part1cubes.items())
print(part1lit)

# part 2
part2cubes = find_lit_cubes(states, coords)
part2lit = sum(v * volume(c) for c, v in part2cubes.items())
print(part2lit)
