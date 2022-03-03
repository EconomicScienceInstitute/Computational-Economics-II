import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

def make_transition_matrix(n_squares):
    # extra square for death
    base_row = np.zeros(n_squares + 1)
    base_row[1:7] = 1/6
    rows = [base_row]
    for i in range(n_squares):
        base_row = np.insert(base_row[:-1], 0, 0)
        rows.append(base_row)
    transition_mat = np.matrix(rows)
    transition_mat[:,-1] = 0
    for i in range(n_squares + 1):
        transition_mat[i,i] = 1 - np.sum(transition_mat[i,:])
    return transition_mat

def make_gif(transition_matrix, n_iterations, base_name):
    # Start at first square
    start_sqr = 0
    state = np.zeros(len(transition_matrix))
    state[start_sqr] = 1
    state = np.matrix([state])

    fig = plt.figure()
    camera = Camera(fig)
    for i in range(n_iterations):
        # Need this in order to plot properly
        state = np.asarray(state).flatten()
        plt.plot(state, 'b')
        plt.ylim([0, 1])
        camera.snap()
        state = state * transition_matrix
    print(state)
    animation = camera.animate()
    animation.save(base_name + '.gif', writer="imagemagick")

def add_chutes_ladders(transition_matrix, chutes_ladders):
    for start, end in chutes_ladders:
        transition_matrix[:, end] += transition_matrix[:, start]
        transition_matrix[:, start] = 0
    return transition_matrix

def average_turns(transition_matrix, n_iterations=1000):
    state = np.zeros(len(transition_matrix))
    state[0] = 1
    state = np.matrix([state])
    prob_done = [state[0, -1]]
    for i in range(n_iterations):
        state = state * transition_matrix
        prob_done.append(state[0, -1])
    prob_finish_turn = np.diff(prob_done)
    mean_turns = 0
    for i in range(n_iterations):
        mean_turns += (i+1) * prob_finish_turn[i]
    return mean_turns

np.set_printoptions(precision=3, suppress=True, linewidth=200)
n_squares = 10
chutes_ladders = [(6, n_squares)]
transition_mat = make_transition_matrix(n_squares)
transition_mat = add_chutes_ladders(transition_mat, chutes_ladders)

Q = transition_mat[:n_squares-1, :n_squares-1]
R = transition_mat[:n_squares-1, n_squares-1:]
# print(transition_mat)
# print(Q)
# print(R)
N = np.linalg.inv(np.eye(n_squares+1 - 2) - Q)
print(N*R)
print(transition_mat**100)

# print(transition_mat)
# print(average_turns(transition_mat))
# make_gif(transition_mat, 100, "chutes_death")
