import pygame
import sys
import numpy as np
from random import randint
from constants import Constants as k

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((k.size), k.flags)
pygame.display.set_caption(k.title)
table = [[0,0,0],[0,0,0],[0,0,0]] # Table is set with 0 for none, 1 for X and 2 for Y

def keyPress():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        sys.exit()

def tictactoeBoard():
    lowerL = pygame.draw.rect(screen, k.black, [k.width/2 - k.rectWidth/2, k.height/2 + k.rectHeight + k.spacing/2, k.rectWidth, k.rectHeight], 0, 4)
    upperL = pygame.draw.rect(screen, k.black, [k.width/2 - k.rectWidth/2, k.height/2 - k.rectHeight - k.spacing/2, k.rectWidth, k.rectHeight], 0, 4)
    leftL = pygame.draw.rect(screen, k.black, [k.width/2 - k.rectHeight - k.spacing/2, k.height/2 - k.rectWidth/2, k.rectHeight, k.rectWidth], 0, 4)
    rightL = pygame.draw.rect(screen, k.black, [k.width/2 + k.rectHeight + k.spacing/2, k.height/2 - k.rectWidth/2, k.rectHeight, k.rectWidth], 0, 4)

    fontLet = pygame.font.SysFont("comicsans", k.letterSize)
    for row in range(3):
        for col in range(3):
            if table[row][col] == 1:
                letter = fontLet.render("X", 1, k.blue)
                screen.blit(letter, (lowerL.x + k.letterSize*(col) + k.rectHeight*((col+1) ** 2), leftL.y - k.rectHeight*((row+1) ** 2) + k.letterSize*2*(row)))
            elif table[row][col] == 2:
                letter = fontLet.render("O", 1, k.blue)
                screen.blit(letter, (lowerL.x + k.letterSize*(col) + k.rectHeight*((col+1) ** 2), leftL.y - k.rectHeight*((row+1) ** 2) + k.letterSize*2*(row)))


def screenUpdate(currentPlayer):
    screen.fill((k.white))

    fontSC = pygame.font.SysFont("comicsans",10) # The DEL button shortcut text
    shortCut = fontSC.render(k.shortCutText, 1, k.red)
    screen.blit(shortCut, (k.width - shortCut.get_width()- 5, k.height - shortCut.get_height() - 5))

    tictactoeBoard() # Displaying the tictactoe board
    winner = checkWinner() # Getting if there is a winner

    fontPlayerTurn = pygame.font.SysFont("comicsans",50)
    fontContinueText = pygame.font.SysFont("comicsans", 25)
    if winner == -1: # The game is still ongoing
        if currentPlayer == 0: # Player's Turn
            playerTurnText = fontPlayerTurn.render("Player Turn", 1, k.black)
            screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
        else: # AI's Turn
            playerTurnText = fontPlayerTurn.render("AI Turn", 1, k.black)
            screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
            continueText = fontContinueText.render("Press click for AI to play", 1, k.black)
            screen.blit(continueText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height() - continueText.get_height() - 10))
    elif winner == 2: # The game was a draw
        playerTurnText = fontPlayerTurn.render("Draw", 1, k.black)
        continueText = fontContinueText.render("Press click to continue", 1, k.black)
        screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
        screen.blit(continueText, (k.width/2 - continueText.get_width()/2, k.height/4 - playerTurnText.get_height() - continueText.get_height() - 10))
    else:
        if winner == 0:
            playerTurnText = fontPlayerTurn.render("Player has won!", 1, k.black)
        elif winner == 1:
            playerTurnText = fontPlayerTurn.render("AI has won!", 1, k.black)
        continueText = fontContinueText.render("Press click to continue", 1, k.black)
        screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
        screen.blit(continueText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height() - continueText.get_height() - 10))

    pygame.display.flip()

    return winner

def getRowColFromMouse(x, y):
    boardLimitUpper = 450
    boardLimitLower = 150
    if boardLimitLower <= x <= boardLimitUpper and boardLimitLower <= y <= boardLimitUpper:
        row = int((y - 150)/100)
        col = int((x - 150)/100)
        return int(row), int(col)
    else:
        return -1, -1

def checkWinner():
    for row in table:
        if row[0] == row[1] == row[2] != 0:
            return row[0] - 1
    for col in range(3):
        if table[0][col] == table[1][col] == table[2][col] != 0:
            return table[0][col] - 1
    if table[0][0] == table[1][1] == table[2][2] != 0:
        return table[0][0] - 1
    if table[0][2] == table[1][1] == table[2][0] != 0:
        return table[0][2] - 1
    for row in table:
        if 0 in row:
            return -1
    return 2

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
    elif depth < 3:  # Depth limit to avoid infinite recursion
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
            elif idx != 4 and idx in corners and priorityMove == -2:
                priorityMove = idx
            elif idx != 4 and idx in edges and priorityMove == -2:
                priorityMove = idx
            elif idx != 4 and ((board[0][0] == 1 and board[2][2] == 1) or (board[0][2] == 1 and board[2][0] == 1)) and idx in edges:
                priorityMove = idx
        return priorityMove
    return move

def main():
    global table
    cl = pygame.time.Clock()
    playerTurn = 0 # Player turn 0, while AI turn 1
    while True:
        cl.tick(60)

        winner = screenUpdate(playerTurn)
        keyPress()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if winner == -1 and playerTurn == 0:
                    mouseX, mouseY = event.pos
                    row, col = getRowColFromMouse(mouseX, mouseY)
                    if row != -1 and col != -1 and table[row][col] == 0:
                        table[row][col] = 1
                        playerTurn = 1
                elif playerTurn == 1 and winner == -1:
                    aiMove = findBestMove(table)
                    row, col = aiMove//3, aiMove%3
                    table[row][col] = 2
                    playerTurn = 0
                else:
                    table = [[0,0,0],[0,0,0],[0,0,0]]
                    playerTurn = 0


if __name__ == "__main__":
    main()