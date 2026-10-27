from collections import deque

# State: (robot_pos, object_pos, holding)
initial_state = ('A', 'C', False)

# Goal: robot membawa objek (atau objek sudah dipindah)
goal_state = ('C', 'C', True)

locations = ['A', 'B', 'C']

def get_actions(state):
    robot_pos, obj_pos, holding = state
    actions = []

    # step 1 : MOVE
    for loc in locations:
        if loc != robot_pos:
            new_state = (loc, obj_pos, holding)
            action = f"Move({robot_pos} -> {loc})"
            actions.append((new_state, action))

    # step 2 : PICK
    if robot_pos == obj_pos and not holding:
        new_state = (robot_pos, obj_pos, True)
        actions.append((new_state, "Pick(Object)"))

    # step 3 : DROP
    if holding:
        new_state = (robot_pos, robot_pos, False)
        actions.append((new_state, "Drop(Object)"))

    return actions


def bfs(initial, goal):
    queue = deque()
    queue.append((initial, []))
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state in visited:
            continue

        visited.add(current_state)

        # Goal check
        if current_state == goal:
            return path

        for next_state, action in get_actions(current_state):
            if next_state not in visited:
                queue.append((next_state, path + [action]))

    return None


# Run BFS
plan = bfs(initial_state, goal_state)

# Output
if plan:
    print("Sequence Plan dari initiate position ke goal ditemukan:")
    for i, step in enumerate(plan, 1):
        print(f"Step {i}: {step}")
else:
    print("Tidak ada solusi")