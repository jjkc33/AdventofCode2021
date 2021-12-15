import numpy as np


def crab_fuel_cost1(positions, x):
    """ Loss function: sum of absolute errors """
    return np.sum(np.abs(positions - x))


def crab_fuel_cost2(positions, x):
    """ Loss function: sum of absolute errors and squared errors """
    part1 = crab_fuel_cost1(positions, x)
    part2 = np.sum((positions - x) ** 2)
    return 0.5 * (part1 + part2)


data = np.loadtxt(r'./input.txt', delimiter=',', max_rows=1)

# part 1

# given that we are taking about absolute errors here
# the optimal solution is to use the median crab position (L1 norm)
median = np.median(data)
answer = crab_fuel_cost1(data, median)
print(answer)


# part 2

# the second loss function can be determined by noting that the
# fuel cost per step can be defined by the sum of n natural numbers, or n * (n + 1) / 2
# defining the loss function as the sum of n * (n + 1) / 2 over all crab submarines
# where n = |y - xi| with y being the optimal position and xi being the position of the ith submarine
# we can simplify this loss function as the sum of the L1 and L2 norms
mean = np.mean(data)
answer2 = min(
    crab_fuel_cost2(data, np.floor(mean)),
    crab_fuel_cost2(data, np.ceil(mean))
)
print(answer2)
