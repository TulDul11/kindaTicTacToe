import numpy as np
from random import randint
import joblib
import pandas as pd
from random import randint
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import os

def checkWinnerNP(flatBoard):
    board = flatBoard.reshape(3, 3)
    
    # Check rows
    for row in board:
        if np.all(row == row[0]) and row[0] != 0:
            return row[0] - 1

    # Check columns
    for col in range(3):
        if np.all(board[:, col] == board[0, col]) and board[0, col] != 0:
            return board[0, col] - 1

    # Check diagonals
    if np.all(np.diag(board) == board[0, 0]) and board[0, 0] != 0:
        return board[0, 0] - 1
    if np.all(np.diag(np.fliplr(board)) == board[0, 2]) and board[0, 2] != 0:
        return board[0, 2] - 1

    # Check for ongoing game
    if np.any(board == 0):
        return -1

    # Return draw
    return 2

def bestAIMove(board, depth):
    flatBoard = np.array(board).flatten()  # Turn board into a flat array
    priorityIDX = -2
    # Try each empty space
    if depth == 0:
        for idx in np.where(flatBoard == 0)[0]:
            temp_board_AI = flatBoard.copy()  # Create a temporary board for the AI move
            temp_board_AI[idx] = 2
            result_AI = checkWinnerNP(temp_board_AI)
            
            if result_AI == 1:  # AI wins
                priorityIDX = idx
    
            temp_board_Player = flatBoard.copy()  # Create a temporary board for the Player move
            temp_board_Player[idx] = 1
            result_Player = checkWinnerNP(temp_board_Player)
            
            if result_Player == 0 and priorityIDX == -2:  # Player wins if this move is taken
                priorityIDX = idx
            
        return priorityIDX
    # Recursively evaluate the move for both AI and Player
    elif depth < 2:  # Depth limit to avoid infinite recursion
        if bestAIMove(temp_board_AI, depth + 1) != -2 or bestAIMove(temp_board_Player, depth + 1) != -2:
            return idx

    return -2  # No immediate win/block, return -2

def findBestMove(board):
    move = bestAIMove(board, 0)
    if move == -2:
        priorityMove = -2
        emptySpaces = np.where(np.array(board).flatten() == 0)[0]
        corners = [0, 2, 6, 8]
        edges = [1, 3, 5, 7]
        for idx in emptySpaces:
            if idx == 4: # If center is empty, take the center
                priorityMove = 4
            elif idx in corners and priorityMove == -2:
                priorityMove = idx
            elif idx in edges and priorityMove == -2:
                priorityMove = idx
            elif ((board[0][0] == 1 and board[2][2] == 1) or (board[0][2] == 1 and board[2][0] == 1)) and idx in edges:
                priorityMove = idx
        return priorityMove
    return move

def generate_random_board():
    num_X = np.random.randint(1, 4)
    num_O = num_X - 1
    board = [[0]*3 for _ in range(3)]

    positions = np.random.choice(range(9), num_X + num_O, replace = False)

    for i in positions[:num_X]:
        board[i//3][i%3] = 1
    for i in positions[num_X:]:
        board[i//3][i%3] = 2

    return board

data = []
for i in range(10000):
    board = generate_random_board()
    bestMove = findBestMove(board)
    flatBoard = [cell for row in board for cell in row]
    data.append(flatBoard + [bestMove])

columns = [f'cell_{i}' for i in range(9)] + ['best_move']
df = pd.DataFrame(data, columns=columns)

# Split into features and target
x = df.drop(columns=['best_move'])  # Features: board state
y = df['best_move']  # Target: best move

# Split into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Save dataset to CSV for future use
model = DecisionTreeClassifier(random_state=42)
model.fit(x_train, y_train)

# Save the model
joblib.dump(model, 'tic_tac_toe_model.pkl')