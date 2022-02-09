from math import inf
n_eggs = 2
n_floors = 100

# create our table
# lookup table by solutions_lookup_table[n_eggs-1][n_floors]
solutions_lookup_table = [[(None, None) for _ in range(n_floors+1)] for _ in range(n_eggs)]

# Base case egg = 1
for j in range(n_floors + 1):
    best_test_floor = 1
    opt_worst_case_num_drops = j
    solutions_lookup_table[0][j] = (best_test_floor, opt_worst_case_num_drops)

# If there are the number of floors is zero
for j in range(n_eggs):
    solutions_lookup_table[j][0] = (0, 0)

for n_eggs_remaining in range(2, n_eggs + 1):
    for n_floors_remaining in range(1, n_floors + 1):
        worst_case_num_drops = inf
        best_test_floor = -1
        for test_floor in range(1, n_floors_remaining + 1):
            # find the best test floor
            solution_if_breaks = 1 + solutions_lookup_table[n_eggs_remaining - 1][test_floor - 1]
            solution_if_intact = 1 + solutions_lookup_table[n_eggs_remaining - 1][n_floors_remaining + 1 - test_floor]
            worst_case_given_floor = max(solution_if_breaks[1],solution_if_intact[1])
            if worst_case_num_drops > worst_case_given_floor:
                # if our worst case overall is bigger than worst case for this floor, we have a new optimal strategy
                worst_case_num_drops = worst_case_given_floor
                best_test_floor = test_floor
        solutions_lookup_table[n_eggs_remaining][n_floors_remaining] = (best_test_floor, worst_case_num_drops)

