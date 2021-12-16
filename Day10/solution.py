
SCORING = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


openers = ['(', '[', '{', '<']
closers = [')', ']', '}', '>']

answer = 0  # part 1 solution
completion_scores = []  # part 2 scores

with open(r'./input.txt') as f:
    for line in f:
        stack = []
        for c in line.strip():
            if c in openers:
                stack.append(c)
            elif stack.pop() != openers[closers.index(c)]:  # part 1
                answer += SCORING[c]
                break
        else:  # part 2
            score = 0
            for c in reversed(stack):
                score = 5 * score + openers.index(c) + 1

            completion_scores.append(score)


# part 1
print(answer)


# part 2
completion_scores.sort()
n_incomplete = len(completion_scores)
answer2 = completion_scores[n_incomplete // 2]
print(answer2)
