import numpy as np

data = np.loadtxt(r'./input.txt')


# part 1
diffs = np.diff(data)
answer = np.sum(diffs > 0)
print(answer)

# part 2
# because the last two numbers in the nth window are the same as the
# first two numbers in the n+1th window we only have to compare the
# first number in the nth window to the last number in the n+1th window
firsts = data[:-3]
lasts = data[3:]
answer2 = np.sum(lasts > firsts)
print(answer2)
