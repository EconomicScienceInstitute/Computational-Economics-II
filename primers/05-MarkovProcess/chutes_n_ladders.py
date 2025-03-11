# https://eleuterio.org/risk-and-reward-lessons-from-chutes-and-ladders/

import numpy as np
import matplotlib.pyplot as plt

LADDER_SQUARES = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    80: 100
}

CHUTES_SQUARES = {
    16: 6,
    47: 26,
    49: 11,
    56: 53,
    62: 19,
    64: 60,
    87: 24,
    93: 73,
    95: 75,
    98: 78,
}

def add_chutes_ladders(transition_matrix: np.matrix, chutes_ladders: dict) -> np.matrix:
    """Add chutes and ladders to the transition matrix

    Args:
        transition_matrix (np.matrix): Transition matrix
        chutes_ladders (dict): Chutes and ladders

    Returns:
        np.matrix: Transition matrix with chutes and ladders
    """
    for start, end in chutes_ladders.items():
        # When you land on 'start', you immediately go to 'end'
        # So we need to redirect all transitions that would lead to 'start'
        # to instead lead to 'end'
        for i in range(transition_matrix.shape[0]):
            # If there's a probability to move from square i to start
            if transition_matrix[i, start] > 0:
                # Add that probability to moving from i to end instead
                transition_matrix[i, end] += transition_matrix[i, start]
                # Remove the probability of moving from i to start
                transition_matrix[i, start] = 0
    return transition_matrix

def make_transition_matrix(n_squares: int) -> np.matrix :
    """Make the transition matrix for a game of chutes and ladders

    Args:
        n_squares (int): Number of squares

    Returns:
        np.matrix: Transition matrix
    """
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
    transition_mat = add_chutes_ladders(transition_mat, CHUTES_SQUARES)
    transition_mat = add_chutes_ladders(transition_mat, LADDER_SQUARES)
    return transition_mat

def create_initial_state(n_squares: int) -> np.matrix:
    """Create the initial state for a game of chutes and ladders

    Args:
        n_squares (int): Number of squares

    Returns:
        np.matrix: Initial state
    """
    initial_state = np.zeros([n_squares + 1])
    initial_state[0] = 1
    return np.matrix(initial_state)

def find_nth_turn(transition_matrix: np.matrix, initial_state: np.matrix, n_turns: int) -> float:
    """Find the probability of finishing the game on the nth turn

    Args:
        transition_matrix (np.matrix): Transition matrix
        initial_state (np.matrix): Initial state
        n_turns (int): Number of turns

    Returns:
        float: Probability of finishing the game on the nth turn
    """
    return np.linalg.matrix_power(transition_matrix.T, n_turns) * initial_state.T

def visualize_nth_turn(transition_matrix: np.matrix, initial_state: np.matrix, n_turns: int, use_opacity: bool = True) -> None:
    """Visualize the state of the game after n
    turns by plotting the state as a heatmap resembling the board

    Args:
        transition_matrix (np.matrix): Transition matrix
        initial_state (np.matrix): Initial state
        n_turns (int): Number of turns
        use_opacity (bool, optional): If True, use opacity for visualization. If False, use color. Defaults to True.
    """
    import plotly.graph_objects as go
    
    state = find_nth_turn(transition_matrix, initial_state, n_turns)[1:]
    state = np.array(state).flatten()  # Convert to flat array for easier indexing
    
    # Create a 10x10 board with proper snake pattern
    board = np.zeros((10, 10))
    square_labels = np.zeros((10, 10), dtype=object)
    
    for i in range(10):
        row = i  # Start from top row (0) and go down
        if i % 2 == 0:  # Even rows go left to right (1-10, 21-30, etc.)
            for j in range(10):
                square_num = i * 10 + j + 1
                board[row, j] = state[square_num - 1]  # -1 for 0-indexing
                square_labels[row, j] = str(square_num)
        else:  # Odd rows go right to left (11-20, 31-40, etc.)
            for j in range(10):
                square_num = (i + 1) * 10 - j
                board[row, j] = state[square_num - 1]  # -1 for 0-indexing
                square_labels[row, j] = str(square_num)
    
    # Create a heatmap with plotly
    if use_opacity:
        # Use a single color with varying opacity
        fig = go.Figure(data=go.Heatmap(
            z=board,
            text=square_labels,
            texttemplate="%{text}",
            colorscale=[[0, 'rgba(0,0,255,0)'], [1, 'rgba(0,0,255,1)']],
            showscale=True,
            colorbar=dict(title="Probability")
        ))
    else:
        # Use color gradient
        fig = go.Figure(data=go.Heatmap(
            z=board,
            text=square_labels,
            texttemplate="%{text}",
            colorscale="Blues",
            showscale=True,
            colorbar=dict(title="Probability")
        ))
    
    fig.update_layout(
        title=f'State after {n_turns} turns',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    fig.show()

def animate_game_states(transition_matrix: np.matrix, initial_state: np.matrix, max_turns: int = 20, use_opacity: bool = True) -> None:
    """Create an animated visualization of the game states with a slider for turn number
    
    Args:
        transition_matrix (np.matrix): Transition matrix
        initial_state (np.matrix): Initial state
        max_turns (int, optional): Maximum number of turns to animate. Defaults to 20.
        use_opacity (bool, optional): If True, use opacity for visualization. If False, use color. Defaults to True.
    """
    import plotly.graph_objects as go
    
    # Create a 10x10 board with proper snake pattern
    square_labels = np.zeros((10, 10), dtype=object)
    
    for i in range(10):
        row = i  # Start from top row (0) and go down
        if i % 2 == 0:  # Even rows go left to right (1-10, 21-30, etc.)
            for j in range(10):
                square_num = i * 10 + j + 1
                square_labels[row, j] = str(square_num)
        else:  # Odd rows go right to left (11-20, 31-40, etc.)
            for j in range(10):
                square_num = (i + 1) * 10 - j
                square_labels[row, j] = str(square_num)
    
    # Set colorscale based on visualization type
    colorscale = [[0, 'rgba(0,0,255,0)'], [1, 'rgba(0,0,255,1)']] if use_opacity else "Blues"
    
    # Create frames for each turn
    frames = []
    for turn in range(max_turns + 1):
        state = find_nth_turn(transition_matrix, initial_state, turn)[1:]
        state = np.array(state).flatten()  # Convert to flat array for easier indexing
        
        board = np.zeros((10, 10))
        for i in range(10):
            if i % 2 == 0:  # Even rows go left to right
                for j in range(10):
                    square_num = i * 10 + j + 1
                    board[i, j] = state[square_num - 1]  # -1 for 0-indexing
            else:  # Odd rows go right to left
                for j in range(10):
                    square_num = (i + 1) * 10 - j
                    board[i, j] = state[square_num - 1]  # -1 for 0-indexing
        
        frames.append(
            go.Frame(
                data=[go.Heatmap(
                    z=board,
                    text=square_labels,
                    texttemplate="%{text}",
                    colorscale=colorscale,
                    showscale=True,
                    colorbar=dict(title="Probability"),
                    zmin=0,
                    zmax=max(0.3, np.max(state))  # Set a reasonable max for color scale
                )],
                name=str(turn),
                layout=go.Layout(title_text=f"State after {turn} turns")
            )
        )
    
    # Initial state for the figure
    initial_state_array = np.array(initial_state).flatten()[1:]
    initial_board = np.zeros((10, 10))
    for i in range(10):
        if i % 2 == 0:
            for j in range(10):
                square_num = i * 10 + j + 1
                initial_board[i, j] = initial_state_array[square_num - 1]
        else:
            for j in range(10):
                square_num = (i + 1) * 10 - j
                initial_board[i, j] = initial_state_array[square_num - 1]
    
    fig = go.Figure(
        data=[go.Heatmap(
            z=initial_board,
            text=square_labels,
            texttemplate="%{text}",
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title="Probability"),
            zmin=0,
            zmax=max(0.3, np.max(initial_state_array))
        )],
        frames=frames,
        layout=go.Layout(
            title="Chutes and Ladders Game State",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}]
                    }
                ],
                "x": 0.1,
                "y": 0,
                "xanchor": "right",
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "steps": [
                    {
                        "label": str(turn),
                        "method": "animate",
                        "args": [[str(turn)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}]
                    }
                    for turn in range(max_turns + 1)
                ],
                "x": 0.1,
                "y": 0,
                "currentvalue": {"prefix": "Turn: ", "visible": True, "xanchor": "right"},
                "len": 0.9,
                "pad": {"b": 10, "t": 50},
                "xanchor": "left",
                "yanchor": "top"
            }]
        )
    )
    
    # Add markers for chutes and ladders
    for start, end in LADDER_SQUARES.items():
        start_row, start_col = (start - 1) // 10, (start - 1) % 10
        if start_row % 2 == 1:  # Odd rows go right to left
            start_col = 9 - start_col
            
        end_row, end_col = (end - 1) // 10, (end - 1) % 10
        if end_row % 2 == 1:  # Odd rows go right to left
            end_col = 9 - end_col
        fig.add_shape(
            type="line",
            x0=start_col,
            y0=start_row,
            x1=end_col,
            y1=end_row,
            line=dict(color="green", width=4),
            opacity=0.8
        )
    
    for start, end in CHUTES_SQUARES.items():
        start_row, start_col = (start - 1) // 10, (start - 1) % 10
        if start_row % 2 == 1:  # Odd rows go right to left
            start_col = 9 - start_col
            
        end_row, end_col = (end - 1) // 10, (end - 1) % 10
        if end_row % 2 == 1:  # Odd rows go right to left
            end_col = 9 - end_col
            
        fig.add_shape(
            type="line",
            x0=start_col,
            y0=start_row,
            x1=end_col,
            y1=end_row,
            line=dict(color="red", width=4),
            opacity=0.8
        )
    
    fig.show()

def visualize_transition_matrix(transition_matrix: np.matrix) -> None:
    """Visualize the transition matrix as a heatmap

    Args:
        transition_matrix (np.matrix): Transition matrix
    """
    plt.imshow(transition_matrix)
    plt.colorbar()
    plt.show()

def main():
    n_squares = 100
    transition_matrix = make_transition_matrix(n_squares)
    initial_state = create_initial_state(n_squares)
    # Animate the game states with a slider for 30 turns
    # Default is to use opacity for visualization
    animate_game_states(transition_matrix, initial_state, max_turns=100, use_opacity=False)

if __name__ == "__main__":
    main()