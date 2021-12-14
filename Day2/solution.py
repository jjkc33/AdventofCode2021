from collections import Counter

# part 1
counter = Counter()

with open(r'./input.txt', mode='r') as f:
    for line in f:
        direction, amount = line.split()
        counter[direction] += int(amount)

depth = counter['down'] - counter['up']
answer = counter['forward'] * depth
print(answer)


# part 2
aim = 0
h_pos = 0
depth = 0

with open(r'./input.txt', mode='r') as f:
    for line in f:
        direction, amount = line.split()
        amount = int(amount)
        if direction == 'down':
            aim += amount
        elif direction == 'up':
            aim -= amount
        else:  # forward
            h_pos += amount
            depth += aim * amount

answer2 = h_pos * depth
print(answer2)
