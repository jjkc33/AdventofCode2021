import numpy as np

with open(r'./input.txt') as f:
    img = []
    for i, line in enumerate(f):
        if i == 0:
            ie_algo = line.strip()
        elif line.strip():
            img.append([int(c == '#') for c in line.strip()])

ie_algo = [int(i == '#') for i in ie_algo]
img = np.array(img, dtype=int)


def kernel2binary(patch):
    powers = 2 ** np.arange(8, -1, -1)
    return np.sum(patch * powers)


enhancements = 50
for e in range(enhancements):
    # fill value alternates between 0 and 1 for each iteration
    padded_img = np.pad(img, 2, constant_values=e % 2)
    n, m = img.shape
    new_img = np.zeros((n + 2, m + 2), dtype=int)
    for i in range(n + 2):
        for j in range(m + 2):
            k = padded_img[i:i + 3, j:j + 3].flatten()
            val = ie_algo[kernel2binary(k)]
            new_img[i, j] = val

    img = new_img

    # part 1 and part 2
    if (e + 1) in (2, 50):
        print(img.sum())

