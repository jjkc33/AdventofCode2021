import numpy as np
from collections import Counter


# 1 has two segments
# 4 has four segments
# 7 has three segments
# 8 has seven segments


# part 1
counter = Counter()

with open(r'./input.txt') as f:
    for line in f:
        _, output = line.split('|')
        counter.update(len(i) for i in output.split())

answer = counter[2] + counter[3] + counter[4] + counter[7]
print(answer)


# part 2

def parse_line(line):
    signal, output = line.split('|')
    signals = [set(s) for s in signal.split()]
    outputs = [set(o) for o in output.split()]
    return signals, outputs


answer2 = 0
with open(r'./input.txt') as f:
    for line in f:
        signal, output = parse_line(line)

        # initialize mapping, the set at the ith position indicates the integer i
        mapping = [None] * 10

        # we can automatically determine digits 1, 4, 7, and 8 based on their lengths
        remaining = []
        for s in signal:
            if len(s) == 2:
                mapping[1] = s
            elif len(s) == 3:
                mapping[7] = s
            elif len(s) == 4:
                mapping[4] = s
            elif len(s) == 7:
                mapping[8] = s
            else:
                remaining.append(s)

        # iterate over signal again to determine remaining digits
        for s in remaining:
            if len(s) == 6:  # determine digits 0, 6, and 9
                if len(mapping[4] - s) == 0:
                    mapping[9] = s
                elif len(mapping[7] - s) == 0:
                    mapping[0] = s
                else:
                    mapping[6] = s
            else:  # determine digits 2, 3, and 5
                if len(mapping[7] - s) == 0:
                    mapping[3] = s
                elif len(mapping[4] - s) == 1:
                    mapping[5] = s
                else:
                    mapping[2] = s

        value = int(''.join([str(mapping.index(o)) for o in output]))
        answer2 += value

print(answer2)
