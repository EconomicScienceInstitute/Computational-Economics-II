from collections import namedtuple
Item = namedtuple("Item", "weight value")
weights = [1,2,3,4,5]
values = [6,8,10,13,17]
items = [Item(w,v) for w,v in zip(weights,values)] # list of all items
cache = {}
State = namedtuple("state","n_items_remaining rem_weight")
MAX_WEIGHT = 9
N_ITEMS = len(items)
for i in range(MAX_WEIGHT + 1):
    temp_state = State(0,i) # no items remaining for any weight
    decision = "N"
    immediate_value = 0
    cache[temp_state] = (immediate_value,decision)

for i in range(N_ITEMS):
    temp_state = State(i,0) # no weight remaining for any items
    decision = "N"
    immediate_value = 0
    cache[temp_state] = (immediate_value,decision)

def solve_knapsack(state):
    if state in cache:
        return cache[state]
    value_included = items[- state.n_items_remaining].value
    weight_included = items[- state.n_items_remaining].weight
    if state.rem_weight < weight_included:
        possible_decisions = ["N"]
    else:
        possible_decisions = ["N", "Y"]
    max_value = - 1
    for decision in possible_decisions:
        if decision == "Y":
            # transition
            new_state = State(n_items_remaining = state.n_items_remaining-1,
                                rem_weight = state.rem_weight - weight_included)
            total_value = value_included + solve_knapsack(new_state)[0]
        else:
            new_state = State(n_items_remaining = state.n_items_remaining-1,
                                rem_weight = state.rem_weight)
            total_value = solve_knapsack(new_state)[0]
        if total_value > max_value:
            max_value = total_value
            cache[state] = (total_value, decision)
    return cache[state]
start_state = State(3,5)
solve_knapsack(start_state)
...
