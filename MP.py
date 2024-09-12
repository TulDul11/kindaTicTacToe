import pygame
import sys
import numpy as np
from constants import Constants as k

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((k.size), k.flags)
pygame.display.set_caption(k.title)
table = [[0,0,0],[0,0,0],[0,0,0]]

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

    fontSC = pygame.font.SysFont("comicsans",10)
    shortCut = fontSC.render(k.shortCutText, 1, k.red)
    screen.blit(shortCut, (k.width - shortCut.get_width()- 5, k.height - shortCut.get_height() - 5))

    tictactoeBoard()
    winner = checkWinner()

    fontPlayerTurn = pygame.font.SysFont("comicsans",50)
    fontContinueText = pygame.font.SysFont("comicsans", 25)
    if winner == -1:
        playerTurnText = fontPlayerTurn.render("Player " + str(currentPlayer + 1), 1, k.black)
        screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
    elif winner == 2:
        playerTurnText = fontPlayerTurn.render("Draw", 1, k.black)
        continueText = fontContinueText.render("Press click to continue", 1, k.black)
        screen.blit(playerTurnText, (k.width/2 - playerTurnText.get_width()/2, k.height/4 - playerTurnText.get_height()))
        screen.blit(continueText, (k.width/2 - continueText.get_width()/2, k.height/4 - playerTurnText.get_height() - continueText.get_height() - 10))
    else:
        playerTurnText = fontPlayerTurn.render("Player " + str(winner + 1) + " has won!", 1, k.black)
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
    if checkDraw():
        return 2
    else:
        return -1

def checkDraw():
    for row in table:
        if 0 in row:
            return False
    return True

def main():
    global table
    cl = pygame.time.Clock()
    playerTurn = 0
    while True:
        cl.tick(60)

        winner = screenUpdate(playerTurn)
        keyPress()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if winner == -1:
                    mouseX, mouseY = event.pos
                    row, col = getRowColFromMouse(mouseX, mouseY)
                    if row != -1 and col != -1 and table[row][col] == 0:
                        if playerTurn == 0:
                            table[row][col] = 1
                            playerTurn += 1
                        else:
                            table[row][col] = 2
                            playerTurn -= 1
                else:
                    table = [[0,0,0],[0,0,0],[0,0,0]]
                    playerTurn = 0

if __name__ == "__main__":
    main()