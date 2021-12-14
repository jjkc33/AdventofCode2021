import numpy as np


# part 1: submarine power consumption

# read file and convert each line into a list of single characters
with open(r'./input.txt', mode='r') as f:
    values = [list(line.strip()) for line in f]


arr = np.array(values).astype(int)
n = arr.shape[0]

# most common element (of 0s and 1s) can be found by
# checking if the column sums are greater than half the array length
col_sums = arr.sum(axis=0)
gamma = 1 * (col_sums >= n // 2)
epsilon = 1 - gamma

# first convert arrays to strings and then strings to binary
gamma_rate = int(''.join(map(str, gamma)), 2)
epsilon_rate = int(''.join(map(str, epsilon)), 2)
answer = gamma_rate * epsilon_rate
print(answer)


# part 2: life support rating of the submarine

def find_valid_index(data, most_common=True):
    """
    Given the input numbers, find the last remaining number that
    follows the correct criteria for each column.
    """
    remaining = data.copy()
    for col_idx in range(arr.shape[1]):
        col = remaining[:, col_idx]

        if most_common:
            idx_to_keep = col.mean() >= 0.5
        else:
            idx_to_keep = col.mean() < 0.5

        remaining = remaining[col == idx_to_keep]
        if remaining.shape[0] == 1:  # exit if only one number left
            break

    return remaining.flatten()

# oxygen generator rating
oxy_rating = find_valid_index(arr)
# convert to decimal
oxy_rating = int(''.join(map(str, oxy_rating)), 2)

# co2 scrubber rating
co2_rating = find_valid_index(arr, most_common=False)
# convert to decimal
co2_rating = int(''.join(map(str, co2_rating)), 2)

answer2 = oxy_rating * co2_rating
print(answer2)
