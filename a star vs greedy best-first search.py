import copy

# in trang thai
def print_state(state):
    for row in state:
        for x in row:
            print(str(x).rjust(2), end=" ")
        print()
    print()


# chuyen doi trang thai
def state_to_tuple(state):
    return tuple(x for row in state for x in row)


def tuple_to_state(tup, n):
    state = []
    for i in range(n):
        state.append(list(tup[i*n:(i+1)*n]))
    return state


# tim o trong
def find_zero(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                return i, j


# heuristic manhattan
def manhattan(state, goal):
    n = len(state)
    pos_goal = {}
    for i in range(n):
        for j in range(n):
            pos_goal[goal[i][j]] = (i, j)

    h = 0
    for i in range(n):
        for j in range(n):
            val = state[i][j]
            if val != 0:
                gi, gj = pos_goal[val]
                h += abs(i - gi) + abs(j - gj)
    return h


# sinh trang thai ke tiep
def get_successors(state):
    n = len(state)
    x, y = find_zero(state)
    successors = []

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            successors.append(new_state)

    return successors


# truy vet duong di
def reconstruct_path(came_from, current, n):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()

    print("so buoc di:", len(path) - 1)
    for i, st in enumerate(path):
        if i == 0:
            print("trang thai ban dau")
        else:
            print("buoc", i)
        print_state(tuple_to_state(st, n))


# greedy best-first search
def greedy_best_first(start, goal):
    n = len(start)
    start_t = state_to_tuple(start)
    goal_t = state_to_tuple(goal)

    open_list = []
    closed = set()
    came_from = {start_t: None}

    h0 = manhattan(start, goal)
    open_list.append((h0, start_t, 0))

    step = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        h, current, g = open_list.pop(0)

        step += 1
        print("buoc ", step, "g =", g, "h =", h, "f =", h)

        if current == goal_t:
            reconstruct_path(came_from, current, n)
            return g, step

        closed.add(current)
        current_state = tuple_to_state(current, n)

        for nxt in get_successors(current_state):
            nxt_t = state_to_tuple(nxt)
            if nxt_t in closed:
                continue
            if nxt_t not in came_from:
                came_from[nxt_t] = current
                h_n = manhattan(nxt, goal)
                open_list.append((h_n, nxt_t, g + 1))

    return None, step


# a* search
def astar(start, goal):
    n = len(start)
    start_t = state_to_tuple(start)
    goal_t = state_to_tuple(goal)

    open_list = []
    closed = set()
    g_score = {start_t: 0}
    came_from = {start_t: None}

    h0 = manhattan(start, goal)
    open_list.append((h0, start_t))

    step = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        f, current = open_list.pop(0)
        g = g_score[current]
        h = f - g

        step += 1
        print("buoc ", step, "g =", g, "h =", h, "f =", f)

        if current == goal_t:
            reconstruct_path(came_from, current, n)
            return g, step

        closed.add(current)
        current_state = tuple_to_state(current, n)

        for nxt in get_successors(current_state):
            nxt_t = state_to_tuple(nxt)
            new_g = g + 1

            if nxt_t in closed:
                continue

            if nxt_t not in g_score or new_g < g_score[nxt_t]:
                g_score[nxt_t] = new_g
                came_from[nxt_t] = current
                h_n = manhattan(nxt, goal)
                f_n = new_g + h_n
                open_list.append((f_n, nxt_t))

    return None, step


# nhap du lieu
def input_puzzle():
    n = int(input("nhap n: "))
    size = n * n

    print("nhap trang thai ban dau (0 la o trong):")
    flat = list(map(int, input().split()))
    start = [flat[i*n:(i+1)*n] for i in range(n)]

    goal_flat = list(range(1, size)) + [0]
    goal = [goal_flat[i*n:(i+1)*n] for i in range(n)]

    return start, goal


# main
if __name__ == "__main__":
    start, goal = input_puzzle()

    print("trang thai dich")
    print_state(goal)

    print("greedy best-first search")
    g_cost, g_steps = greedy_best_first(start, goal)

    print("a* search")
    a_cost, a_steps = astar(start, goal)

    print("so sanh")
    print("greedy: so buoc =", g_cost, "so lan mo rong =", g_steps)
    print("a*: so buoc =", a_cost, "so lan mo rong =", a_steps)
