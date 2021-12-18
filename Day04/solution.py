import numpy as np


numbers = np.loadtxt(r'./input.txt', dtype=int, delimiter=',', max_rows=1)
boards = np.loadtxt(r'./input.txt', dtype=int, skiprows=1)
boards = boards.reshape((-1, 5, 5))  # (num_boards, height, width)
masks = np.zeros(boards.shape, dtype=int)


def check_for_winning_board(mask):
    return (mask.all(axis=1) | mask.all(axis=2)).any(axis=1)


first_win = False
past_winning_boards = None
for n in numbers:
    masks[boards == n] = 1
    winning = check_for_winning_board(masks)
    # part 1
    if winning.any() and not first_win:
        first_win = True
        winning_board = boards[winning]
        winning_mask = masks[winning]
        board_sum = np.sum(winning_board * (1 - winning_mask))
        answer = n * board_sum

    # part 2
    if winning.all():
        last_winning_board = np.argwhere(winning > past_winning_boards)
        winning_board = boards[last_winning_board]
        winning_mask = masks[last_winning_board]
        board_sum = np.sum(winning_board * (1 - winning_mask))
        answer2 = n * board_sum
        break

    # keep track of prior winning boards to identify last winning board
    past_winning_boards = winning

print(answer)
print(answer2)
