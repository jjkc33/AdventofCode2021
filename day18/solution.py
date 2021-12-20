import re
import ast


def add(n1, n2):
    return f'[{n1},{n2}]'


def explode_left(n, left_num):
    m = re.search(r'\d+', n[::-1])
    if m is None:
        return n + '0'
    idx1, idx2 = -m.end(), -m.start()
    reg_num = n[idx1:idx2]
    return n[:idx1] + str(int(reg_num) + int(left_num)) + n[idx2:] + '0'


def explode_right(n, right_num):
    m = re.search(r'\d+', n)
    if m is None:
        return n
    idx1, idx2 = m.start(), m.end()
    reg_num = n[idx1:idx2]
    return n[:idx1] + str(int(reg_num) + int(right_num)) + n[idx2:]


def is_pair(p):
    if p[0] != '[' or p[-1] != ']':
        return False
    return p[1].isdigit() and p[-2].isdigit()


def reduce(n):
    depth = 0
    new = ''
    # pair_idx = (0, 0)
    for i in range(len(n)):
        if is_pair(n[i:i + 5]) and depth >= 4:
            new = explode_left(new, n[i + 1]) + explode_right(n[i + 5:], n[i + 3])
            break

        c = n[i]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1

        # append character to new string
        # if i not in range(*pair_idx):
        new += c
    else:  # no explodes, check for splits
        nums = re.findall(r'\d+', n)
        for num in nums:
            num = int(num)
            if num > 9:
                idx = n.find(str(num))
                new_pair = f'[{num // 2},{num // 2 + num % 2}]'
                new = n[:idx] + new_pair + n[idx + 2:]
                break
    return new


with open(r'./input.txt') as f:
    numbers = [line.strip() for line in f]


number = numbers[0]
for i, num in enumerate(numbers[1:]):
    new = add(number, num)
    while True:
        new2 = reduce(new)
        if new2 == new:
            break
        new = new2

    number = new


def magnitude(num):
    if isinstance(num, int):
        return num
    else:
        return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


print(number, magnitude(ast.literal_eval(number)))
# [[[[6,6],[7,7]],[[6,7],[6,7]]],[[[6,6],[6,0]],[[7,8],[8,8]]]] 3920