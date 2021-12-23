
rooms = []
with open(r'./input.txt') as f:
    for i, line in enumerate(f):
        if i == 1:
            hallway = line.strip().replace('#', '')
        elif i in (2, 3):
            rooms.append(line.strip().replace('#', ''))


print(hallway)
print(rooms)

rooms = 'BACDBCDA'

state = ('.', '.', ('B', 'A'), '.', ('C', 'D'), '.', ('B', 'C'), '.', ('D', 'A'), '.', '.')
END_STATE = ('.', '.', ('A', 'A'), '.', ('B', 'B'), '.', ('C', 'C'), '.', ('D', 'D'), '.', '.')

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


# def open_hallway_spots(s):
#     hallway, rooms = s
#     open_spots = []
#     for i in (0, 1, 3, 5, 7, 9, 10):  # cannot stop above a room (even numbers)
#         if hallway[i] == '.':
#             open_spots.append(i)
#
#     return open_spots
#
#
# def open_room_spots(s):
#     hallway, rooms = s
#     open_spots = []
#     if rooms.isalpha():  # all rooms full
#         return open_spots
#
#     for i, c in enumerate(rooms):
#         if c == '.':
#             open_spots.append(i)
#
#     return open_spots
#
#
# def movable_amphipods_old(s):
#     hallway, rooms = s
#
#     room_amphipods = []
#     for i in range(0, len(rooms), 2):
#         if rooms[i + 1] == GOAL[i + 1]:  # back space of room is correct
#             if rooms[i] == GOAL[i]:  # front space of room is correct
#                 continue
#             elif rooms[i] != '.':  # front space is not empty
#                 room_amphipods.append((rooms[i], i))
#         elif rooms[i] == '.':  # front space is empty
#             room_amphipods.append((rooms[i + 1], i + 1))
#         else:
#             room_amphipods.append((rooms[i], i))
#
#     hallway_amphipods = []
#     for i, c in enumerate(hallway):
#         if c != '.':  # amphipod in hallway space
#             hallway_amphipods.append((c, i))
#
#     return hallway_amphipods, room_amphipods


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
                        moves.append((i, j))
                        break
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
                        moves.append((i, j))
                        break
        elif space != '.':  # hallway blocked
            break
        elif in_room and space == '.':
            moves.append((i, -1))

    return moves


def organize_amphipods(state):
    if state == END_STATE:
        return 0

    costs = []
    for next_state, cost in available_moves(state):
        print(next_state)
        new_cost = cost + organize_amphipods(next_state)
        costs.append(new_cost)

    return costs

print(state)
costs = organize_amphipods(state)
print(min(costs))
