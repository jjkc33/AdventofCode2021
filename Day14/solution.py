from collections import Counter


insertions = {}

with open(r'./input.txt') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if i == 0:
            polymer = line
        elif line:
            pair, value = line.split(' -> ')
            insertions[pair] = value


# get counts of each unique adjacent pair in polymer string
current_pairs = Counter()
for i in range(len(polymer) - 1):
    current_pairs[polymer[i:i + 2]] += 1


steps = 40
for i in range(steps):
    next_pairs = Counter()
    for pair, cnt in current_pairs.items():
        value = insertions[pair]
        next_pairs[pair[0] + value] += cnt
        next_pairs[value + pair[1]] += cnt

    current_pairs = next_pairs
    if i == 9:  # part 1
        counts1 = Counter(polymer[-1])
        for pair, cnt in current_pairs.items():
            counts1[pair[0]] += cnt

        # part 1
        most_common = counts1.most_common()
        answer = most_common[0][-1] - most_common[-1][-1]
        print(answer)

counts2 = Counter(polymer[-1])
for pair, cnt in current_pairs.items():
    counts2[pair[0]] += cnt

# part 2
most_common = counts2.most_common()
answer2 = most_common[0][-1] - most_common[-1][-1]
print(answer2)
