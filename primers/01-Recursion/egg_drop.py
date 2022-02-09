n_floors = 100
n_eggs = 5

opt_worst_case = [[None] * (n_floors+1) for _ in range(n_eggs)]
opt_worst_case[0] = [(1, i) for i in range(n_floors + 1)]
for i in range(n_eggs):
    opt_worst_case[i][0] = (0,0)

for k in range(1, n_eggs):
    for n_rem_floors in range(1, n_floors + 1):
        best_floor = -1
        opt_worst = n_floors + 1
        for test_floor in range(1, n_rem_floors + 1):
            n_if_break = 1 + opt_worst_case[k-1][test_floor-1][1]
            n_if_survive = 1 + opt_worst_case[k][n_rem_floors - test_floor][1]
            worst_case = max(n_if_break, n_if_survive)
            if worst_case < opt_worst:
                best_floor = test_floor
                opt_worst = worst_case
        opt_worst_case[k][n_rem_floors] = (best_floor, opt_worst)
n = 0
for col in zip(*opt_worst_case):
    print(n, col)
    n+=1
