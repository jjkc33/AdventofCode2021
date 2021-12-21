import ast
from itertools import combinations, permutations
from collections import defaultdict


scanners = []
with open(r'./input.txt') as f:
    beacons = []
    for line in f:
        if line.strip():
            if 'scanner' in line:
                if beacons:
                    scanners.append(beacons)
                beacons = []
            else:
                beacons.append(ast.literal_eval(line.strip()))
    scanners.append(beacons)


def beacon_relative_position(b1, b2):
    return tuple(d1 - d2 for d1, d2 in zip(b1, b2))


def manhattan_distance(b1, b2):
    return sum(abs(d1 - d2) for d1, d2 in zip(b1, b2))


def euclidean_distance(b1, b2):
    return sum((d1 - d2) ** 2 for d1, d2 in zip(b1, b2))


def beacon_distances(b1, b2):
    d1 = manhattan_distance(b1, b2)
    d2 = euclidean_distance(b1, b2)
    return d1, d2


def find_rel_beacon_pos(beacons):
    beacon_coords = defaultdict(set)
    for i, j in combinations(range(len(beacons)), 2):
        dist = beacon_distances(beacons[i], beacons[j])
        beacon_coords[i].add(dist)
        beacon_coords[j].add(dist)
    return beacon_coords


def basis_transforms():
    flips = [
        (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
    ]
    for shifts in permutations(range(3), 3):
        for flip in flips:
            yield lambda x: tuple(x[shifts[i]] * flip[shifts[i]] for i in range(3))


def rotate_and_shift(basis, shift, coords):
    coords = basis(coords)
    return tuple(c + s for c, s in zip(coords, shift))

# start with first beacon
found_beacons = scanners[0]
scanner_indices = list(range(1, len(scanners)))
while scanner_indices:
    left_over = []
    for i in scanner_indices:
        beacons = scanners[i]

        found_beacons_rel = find_rel_beacon_pos(found_beacons)
        beacons_rel = find_rel_beacon_pos(beacons)

        matching_beacons = []
        for b1_idx, b1_coords in beacons_rel.items():
            for b2_idx, b2_coords in found_beacons_rel.items():
                if len(b1_coords & b2_coords) >= 11:
                    matching_beacons.append([found_beacons[b2_idx], beacons[b1_idx]])
                    break

        additional_beacons = []
        if matching_beacons:
            for trans in basis_transforms():
                translations = {beacon_relative_position(b1, trans(b2)) for b1, b2 in matching_beacons}
                if len(translations) == 1:
                    shift = translations.pop()
                    additional_beacons = [rotate_and_shift(trans, shift, b) for b in beacons]
                    break

            found_beacons.extend(additional_beacons)
        else:
            left_over.append(i)

    scanner_indices = left_over


# part 1
print(len(set(found_beacons)))
