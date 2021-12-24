from functools import lru_cache


# TODO clean up functions, reduce duplicate code
# TODO alternative solution: replace DFS + memoization with BFS + priority queue


GOALS = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}

COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def build_initial_state(hallway, rooms):
    state = []
    for i in range(len(hallway)):
        if i in (2, 4, 6, 8):  # room
            room = []
            for j in range(len(rooms)):
                room.append(rooms[j][i // 2 - 1])
            state.append(tuple(room))
        else:
            state.append('.')

    return tuple(state)


def available_moves(s: tuple):
    moves = movable_amphipods(s)
    for amphipod, old_loc, moveset in moves:
        for move in moveset:
            new_state = create_new_state(s, amphipod, old_loc, move)
            cost = move_cost(amphipod, old_loc, move)
            yield new_state, cost


def move_cost(pod_type: str, old_pos: tuple, new_pos: tuple):
    energy = COSTS[pod_type]
    x1, y1 = old_pos
    x2, y2 = new_pos
    steps = abs(x2 - x1)
    if y1 != -1:  # started in a room
        steps += y1 + 1
    if y2 != -1:  # ended in a room
        steps += y2 + 1
    return energy * steps


def create_new_state(old_state: tuple, pod_type: str, old_pos: tuple, new_pos: tuple):
    new_state = []
    for i, c in enumerate(old_state):
        if isinstance(c, tuple):  # room
            if i == old_pos[0]:
                old_room = []
                for j in range(len(c)):
                    if j == old_pos[-1]:
                        old_room.append('.')
                    else:
                        old_room.append(c[j])
                new_state.append(tuple(old_room))
            elif i == new_pos[0]:
                new_room = []
                for j in range(len(c)):
                    if j == new_pos[-1]:
                        new_room.append(pod_type)
                    else:
                        new_room.append(c[j])
                new_state.append(tuple(new_room))
            else:
                new_state.append(c)
        else:  # hallway
            if i == old_pos[0]:  # set old position to empty
                new_state.append('.')
            elif i == new_pos[0]:  # set new position to occupied
                new_state.append(pod_type)
            else:
                new_state.append(c)

    return tuple(new_state)


def movable_amphipods(s: tuple):
    pods = []
    for i, c in enumerate(s):
        if isinstance(c, tuple):  # a room
            move_from_room = False
            # determine if wrong ordering of amphipods is present
            for j in range(len(c) - 1, -1, -1):
                pod = c[j]
                if pod == '.':  # empty room
                    break
                elif i != GOALS[pod]:  # amphipod is in wrong room
                    move_from_room = True
                    break

            if move_from_room:
                for j, r in enumerate(c):
                    if r != '.':  # room space occupied
                        moves = eligible_moves(s, r, i)
                        pods.append((r, (i, j), moves))
                        break
        elif c != '.':  # hallway space occupied
            moves = eligible_moves(s, c, i)
            pods.append((c, (i, -1), moves))

    return pods


def eligible_moves(s: tuple, pod_type: str, pod_idx: int):
    """Find any eligible spaces in the hallway OR correct room"""
    in_room = pod_idx in (2, 4, 6, 8)
    moves = []
    # check moves to the right
    for i in range(pod_idx + 1, len(s)):
        space = s[i]
        if isinstance(space, tuple):
            if i == GOALS[pod_type]:  # correct room
                for j in range(len(space) - 1, -1, -1):  # find furthest open space
                    if space[j] == '.':
                        return [(i, j)]
                    elif space[j] != pod_type:
                        break
        elif space != '.':  # hallway blocked
            break
        elif in_room and space == '.':
            moves.append((i, -1))

    # check moves to the left
    for i in range(pod_idx - 1, -1, -1):
        space = s[i]
        if isinstance(space, tuple):
            if i == GOALS[pod_type]:  # correct room
                for j in range(len(space) - 1, -1, -1):  # find furthest open space
                    if space[j] == '.':
                        return [(i, j)]
                    elif space[j] != pod_type:
                        break
        elif space != '.':  # hallway blocked
            break
        elif in_room and space == '.':
            moves.append((i, -1))

    return moves


@lru_cache(maxsize=2 ** 20)
def organize_amphipods_part1(state):
    if state == END_STATE_P1:
        return 0

    costs = [2**63 - 1]
    for next_state, cost in available_moves(state):
        new_cost = cost + organize_amphipods_part1(next_state)
        costs.append(new_cost)

    return min(costs)


@lru_cache(maxsize=2 ** 21)
def organize_amphipods_part2(state):
    if state == END_STATE_P2:
        return 0

    costs = [2**63 - 1]
    for next_state, cost in available_moves(state):
        new_cost = cost + organize_amphipods_part2(next_state)
        costs.append(new_cost)

    return min(costs)


rooms = []
with open(r'./input.txt') as f:
    for i, line in enumerate(f):
        if i == 1:
            hallway = line.strip().replace('#', '')
        elif i in (2, 3):
            rooms.append(line.strip().replace('#', ''))


# part 1
END_STATE_P1 = ('.', '.', ('A', 'A'), '.', ('B', 'B'), '.', ('C', 'C'), '.', ('D', 'D'), '.', '.')

state = build_initial_state(hallway, rooms)
print(state)
answer = organize_amphipods_part1(state)
print(answer)

# part 2
END_STATE_P2 = ('.', '.', ('A', 'A', 'A', 'A'), '.', ('B', 'B', 'B', 'B'),
                '.', ('C', 'C', 'C', 'C'), '.', ('D', 'D', 'D', 'D'), '.', '.')


rooms.insert(1, 'DCBA')
rooms.insert(2, 'DBAC')

state2 = build_initial_state(hallway, rooms)
print(state2)
answer2 = organize_amphipods_part2(state2)
print(answer2)
