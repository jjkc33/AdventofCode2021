import re
import itertools


states, coords = [], []
with open(r'./input.txt') as f:
    for line in f:
        state, nums = line.split()
        nums = re.findall('-?\d+', nums)
        states.append(int(state == 'on'))
        coords.append(tuple(int(n) for n in nums))


# part 1
lights = set()
for s, c in zip(states, coords):
    if any(abs(i) > 50 for i in c):
        continue

    x1, x2, y1, y2, z1, z2 = c
    positions = {pos for pos in itertools.product(range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1))}
    if s == 1:  # on
        lights.update(positions)
    else:  # off
        lights.difference_update(positions)

print(len(lights))
