
SCORING = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

# part 1
openers = ['(', '[', '{', '<']
closers = [')', ']', '}', '>']
answer = 0

with open(r'./input.txt') as f:
    for line in f:
        stack = []
        for c in line.strip():
            if c in openers:
                stack.append(c)
            elif stack.pop() != openers[closers.index(c)]:
                answer += SCORING[c]

print(answer)
