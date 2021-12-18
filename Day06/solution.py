from collections import deque

with open(r'./input.txt')as f:
    fishes = list(map(int, f.read().split(',')))


max_age = 8
days = 256

# count of fish at each age
ages = deque([fishes.count(i) for i in range(max_age + 1)], maxlen=max_age + 1)

# rotate queue on each day, decrementing each fish timer
# and set the zeroed timers back to 6
for i in range(days):
    if i == 80:
        print(sum(ages))
    new_fishes = ages.popleft()
    ages.append(new_fishes)
    ages[6] += new_fishes

# part 2
print(sum(ages))
