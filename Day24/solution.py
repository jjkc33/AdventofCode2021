from functools import lru_cache

instructions = []
with open(r'./input.txt') as f:
    rules = []
    for i, line in enumerate(f):
        instr, *v = line.strip().split()
        if i != 0 and instr == 'inp':
            instructions.append(rules)
            rules = []
        rules.append(line.strip())  # (instr, *v))

    # append final instruction set
    instructions.append(rules)

nrows = len(instructions[0])
ncols = len(instructions)
for row in range(nrows):
    s = [instructions[col][row].ljust(10) for col in range(ncols)]
    print(' '.join(s))

"""
By printing out the instructions in a tabular format a clear pattern emerges.
For each digit, w, in the 14-digit model number, the following applies:

inp w
mul x 0
add x z
mod x 26
div z A     *
add x B     *
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y C     *
mul y x
add z y

Where A, B, and C are variables taking certain values under given conditions.

Simplifying these rules into mathematical formulas yields the following:

w = input digit
x = (z % 26) + B != w  # 1 or 0
z = (z / A) * (25 * x + 1) + (w + C) * x

For each input digit, w is always set to that digit. 
Variables x and y are always reset to 0, essentially acting as placeholders during calculations.
z is the only variable persisted across input digits.

The variable A takes one of two possible values, 1 or 26, equally.
(i.e. For 7 digits, A = 1. For the remaining 7 digits, A = 26.)

When A = 1, B is always positive, taking values between 10 and 15
When A = 26, B is always negative, taking values between -11 and -3

C is a positive integer between 1 and 16 for each input digit.


"""

A = [1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 1, 26, 26, 26]
B = [13, 13, 10, 15, -8, -10, 11, -3, 14, -4, 14, -5, -8, -11]
C = [15, 16, 4, 14, 1, 5, 1, 3, 3, 7, 5, 13, 3, 10]


# determine maximum z value at each input digit
max_Z_values = []
pow = 7  # starts at 26 ** 7
for a in A:
    max_Z_values.append(26 ** pow)
    if a == 26:
        pow -= 1


@lru_cache(maxsize=2 ** 20)
def solve2(idx, z, s):
    if idx == 14:
        print(s, z)
        return s

    if z > max_Z_values[idx]:
        return s
    # get values for current input digit
    a, b, c = A[idx], B[idx], C[idx]

    # test if x can be 0 (best case b/c z remains small)
    prev_z = z * a
    w = (prev_z % 26) + b
    if w in range(1, 10):
        return solve2(idx + 1, prev_z, str(w) + s)
    else:
        num_strs = []
        for w in range(9, 0, -1):
            prev_z = a * (z - w - c) // 26
            num_strs.append(solve2(idx + 1, prev_z, str(w) + s))

        return str(max(int(i) for i in num_strs))


@lru_cache(maxsize=2 ** 20)
def solve3(idx, z):
    if idx == 14:
        if z == 0:
            return ['']
        return []

    if z > max_Z_values[idx]:
        return []

    # get values for current input digit
    a, b, c = A[idx], B[idx], C[idx]

    # test if x can be 0 (best case b/c z remains small)
    w = (z % 26) + b
    numbers = []
    if w in range(1, 10):
        model_nums = solve3(idx + 1, z // a)
        for n in model_nums:
            numbers.append(str(w) + n)
    else:
        for w in range(9, 0, -1):
            model_nums = solve3(idx + 1, 26 * z // a + w + c)
            for n in model_nums:
                numbers.append(str(w) + n)

    return numbers


# val = solve2(idx=13, z=0, s='')
solutions = solve3(idx=0, z=0)
solutions = [int(x) for x in solutions]

# part 1
print(max(solutions))

# part 2
print(min(solutions))


@lru_cache(maxsize=2 ** 20)
def solve4(idx, z):
    if idx == 14:
        if z == 0:
            return ''
        return None

    if z > max_Z_values[idx]:
        return None

    # get values for current input digit
    a, b, c = A[idx], B[idx], C[idx]

    # test if x can be 0 (best case b/c z remains small)
    w = (z % 26) + b
    if w in range(1, 10):
        s = solve4(idx + 1, z // a)
        if s is not None:
            return str(w) + s
    else:
        num_strs = []
        for w in range(9, 0, -1):
            s = solve4(idx + 1, 26 * z // a + w + c)
            if s is not None:
                num_strs.append(str(w) + s)

        if num_strs:
            return str(max(int(i) for i in num_strs))

print(solve4(0, 0))
