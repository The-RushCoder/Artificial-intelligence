import random
import math
import copy

# Generate random number between 0 to 1
random.seed(100)

"""
# Generate random numbers
for i in range(5):
    print(random.random())
"""

# List copy function
def deepcopy(state):
    return [row[:] for row in state]

# Heuristic function h1: Misplaced tiles
def h1(state):
    goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j]:
                misplaced += 1
    return misplaced

# Heuristic function h2: Manhattan distance
def h2(state):
    goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x_goal, y_goal = divmod(goal_state[i][j], 3)
                x_state, y_state = divmod(state[i][j], 3)
                distance += abs(x_goal - x_state) + abs(y_goal - y_state)
    return distance

# Get the lowest cost successor
def get_lowest_cost_successor(curr_state, heuristic_func):
    successors = []
    blank_i, blank_j = [(i, j) for i in range(3) for j in range(3) if curr_state[i][j] == 0][0]
    for move_i, move_j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if 0 <= blank_i + move_i < 3 and 0 <= blank_j + move_j < 3:
            neighbor_state = deepcopy(curr_state)
            neighbor_state[blank_i][blank_j], neighbor_state[blank_i + move_i][blank_j + move_j] = \
                neighbor_state[blank_i + move_i][blank_j + move_j], neighbor_state[blank_i][blank_j]
            successors.append(neighbor_state)

    min_cost = float('inf')
    min_state = None
    for successor in successors:
        cost = heuristic_func(successor)
        if cost < min_cost:
            min_cost = cost
            min_state = successor
    return min_state, min_cost

# Steepest Ascent Hill Climbing Algorithm
def hill_climbing(start_state, heuristic_func):
    curr_state = start_state
    itr = 0
    while True:
        itr += 1
        if itr > 1000:
            break
        neighbor, neighbor_cost = get_lowest_cost_successor(curr_state, heuristic_func)
        #print(f"Neighbor {neighbor} h={neighbor_cost}")
        print(f"Current {curr_state} h={heuristic_func(curr_state)}")
        if neighbor_cost >= heuristic_func(curr_state):
            print(f"Neighbor {neighbor} h={neighbor_cost}")
            return curr_state
        curr_state = neighbor
    return curr_state

# Simulated Annealing Algorithm
def simulated_annealing(start_state, heuristic_func, schedule_func):
    curr_state = start_state
    t = 1
    while True:
        T = schedule_func(t)
        if T == 0:
            return curr_state
        neighbor, neighbor_cost = get_lowest_cost_successor(curr_state, heuristic_func)
        delta_E = neighbor_cost - heuristic_func(curr_state)
        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            curr_state = neighbor
        t += 1

# Schedule function for Simulated Annealing
def schedule(t):
    return max(0, 500 - t)

# Test the algorithms

#start_state = [[3, 1, 2], [0, 4, 5], [6, 7, 8]]    #Input-1
start_state = [[3, 1, 2], [6, 4, 0], [7, 8, 5]]    #Input-2
goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]    #Goal State


print("Hill Climbing with Misplaced Tiles Heuristic:")
final_state_h1 = hill_climbing(start_state, h1)
print(f"Solution {final_state_h1} h={h1(final_state_h1)}")

"""
print("Hill Climbing with Manhattan Distance Heuristic:")
final_state_h2 = hill_climbing(start_state, h2)
print(f"Solution {final_state_h2} h={h2(final_state_h2)}")

print("Simulated Annealing with Misplaced Tiles Heuristic:")
final_state_sa_h1 = simulated_annealing(start_state, h1, schedule)
print(f"Solution {final_state_sa_h1} h={h1(final_state_sa_h1)}")

print("Simulated Annealing with Manhattan Distance Heuristic:")
final_state_sa_h2 = simulated_annealing(start_state, h2, schedule)
print(f"Solution {final_state_sa_h2} h={h2(final_state_sa_h2)}")
"""