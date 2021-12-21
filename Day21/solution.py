import itertools
from functools import lru_cache


def roll(die):
    return sum(next(die) for _ in range(3))


with open(r'./input.txt') as f:
    starting_pos = [int(l.strip()[-1]) for l in f]


die = itertools.cycle(range(1, 101))  # infinite die rolls in [1, 100]
roll_count = 0
winning_score = 1000
p1, p2 = starting_pos
p1_score, p2_score = 0, 0

while p1_score < 1000 and p2_score < 1000:
    roll_count += 3
    move = roll(die)
    if move % 2 == 0:  # player 1
        p1 = (p1 + move - 1) % 10 + 1
        p1_score += p1
    else:
        p2 = (p2 + move - 1) % 10 + 1
        p2_score += p2


# part 1
answer = min(p1_score, p2_score) * roll_count
print(answer)

# part 2


"""
outcomes of 3 sided die, rolled thrice
    3: 1/27
    4: 3/27
    5: 6/27
    6: 7/27
    7: 6/27
    8: 3/27
    9: 1/27
"""


# 10 positions for both p1 and p2, 21 scores for both p1 and p2
@lru_cache(maxsize=10*10*21*21)
def quantum(p1_pos, p1_score, p2_pos, p2_score):
    if p1_score > 20:
        return 1, 0
    elif p2_score > 20:
        return 0, 1

    wins = 0, 0
    for die in itertools.product(range(1, 4), repeat=3):
        pos_ = (p1_pos + sum(die) - 1) % 10 + 1
        score_ = p1_score + pos_
        w2, w1 = quantum(p2_pos, p2_score, pos_, score_)
        wins = wins[0] + w1, wins[1] + w2

    return wins

# part 2
p1, p2 = starting_pos
p1_score, p2_score = 0, 0
score = quantum(p1, p1_score, p2, p2_score)
print(max(score))
