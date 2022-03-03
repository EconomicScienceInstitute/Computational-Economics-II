import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from collections import Counter


def get_probabilities():
    """
    Gets probabilities for dice rolls for two dice
    :return: list of probabilities
    """
    vals = np.arange(1, 7)
    probs = Counter([i + j for i in vals for j in vals])
    return [0, 0] + [count / 36 for count in probs.values()]


def make_transition_matrix(n_squares: int):
    """ creates transition matrix for monopoly game with n_squares
    n_squares
    """
    base_row = np.zeros(n_squares + 1)
    base_row[0:13] = get_probabilities()
    rows = [base_row]
    for i in range(n_squares):
        base_row = np.insert(base_row[:-1], 0, 0)
        rows.append(base_row)
    transition_mat = np.matrix(rows)
    # for i in range(n_squares + 1):
    #     transition_mat[i, i] = 1 - np.sum(transition_mat[i, :])
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
        plt.ylim([0, .2])
        camera.snap()
        state = state * transition_matrix
    print(state)
    animation = camera.animate()
    animation.save(base_name + '.gif', writer="imagemagick")

if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=True, linewidth=200)
    trans_mat = make_transition_matrix(40)
    make_gif(trans_mat,500,"monopoly")
