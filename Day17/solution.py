import re

with open(r'./input.txt') as f:
    data = f.readline().strip()


coords = re.findall(r'-?\d+', data)
coords = [int(c) for c in coords]
print(coords)


xmin, xmax, ymin, ymax = coords


def step(pos, velocity):
    xpos, ypos = pos
    xvel, yvel = velocity

    xpos += xvel
    ypos += yvel

    if xvel > 0:
        xvel -= 1
    elif xvel < 0:
        xvel += 1

    yvel -= 1
    return (xpos, ypos), (xvel, yvel)


def test_launch(pos, vel):
    target_hit = False
    steps = 0
    max_height = 0
    while not target_hit:
        pos, vel = step(pos, vel)
        max_height = max(max_height, pos[1])
        steps += 1

        if pos[0] in range(xmin, xmax + 1) and pos[1] in range(ymin, ymax + 1):
            target_hit = True
        elif pos[0] > xmax:
            break
        elif pos[1] < ymin:
            break

    return max_height, target_hit


heights = []
for x in range(xmax + 1):
    for y in range(ymin - 1, abs(ymin) + 1):
        height, hit = test_launch((0, 0), (x, y))
        if hit:
            heights.append(height)

print(max(heights))
print(len(heights))
